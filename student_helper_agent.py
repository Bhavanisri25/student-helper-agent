"""
Exercise 2: Student Helper Agent
------------------------------------
Classifies a student's query as needing math help, Python syntax help,
or English grammar correction, then routes to the matching tool -
with human-in-loop confirmation and error-safe invocation.
"""
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
load_dotenv(dotenv_path=Path(__file__).parent / ".env")
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
SYSTEM_PROMPT = (
    "You are a tool-routing classifier for a student helper agent. "
    "Classify the user's query into exactly one of these three labels: "
    "math, python_help, or english_grammar. "
    "math = arithmetic or numeric calculation requests. "
    "python_help = Python syntax, errors, or how-to-code questions. "
    "english_grammar = requests to check or correct English grammar/sentences. "
    "Respond with ONLY the single label word, nothing else."
)


# ---------------------------------------------------------------
# TOOL 1: math - safely evaluates a simple arithmetic expression
# ---------------------------------------------------------------
def math_tool(query: str) -> str:
    expression = "".join(re.findall(r"[\d\.\+\-\*\/\(\)\s]+", query)).strip()
    if not expression:
        return "I couldn't find a valid math expression in your query."
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {expression.strip()} = {result}"
    except Exception:
        return "Sorry, I couldn't safely evaluate that expression."


# ---------------------------------------------------------------
# TOOL 2: python_help - looks up a canned explanation for common topics
# ---------------------------------------------------------------
PYTHON_HELP = {
    "list": "A list is an ordered, changeable collection: my_list = [1, 2, 3]",
    "loop": "Use 'for item in sequence:' or 'while condition:' to repeat code.",
    "function": "Define with 'def name(params):' and return a value with 'return'.",
    "dictionary": "A dictionary stores key-value pairs: my_dict = {'key': 'value'}",
    "error": "Check the last line of the traceback - it usually names the exact issue.",
}

def python_help_tool(query: str) -> str:
    query_lower = query.lower()
    for keyword, explanation in PYTHON_HELP.items():
        if keyword in query_lower:
            return f"[Python Help - {keyword}] {explanation}"
    return "[Python Help] Try rephrasing with a specific topic like 'list', 'loop', or 'function'."


# ---------------------------------------------------------------
# TOOL 3: english_grammar - uses the LLM to correct grammar
# ---------------------------------------------------------------
def english_grammar_tool(query: str) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "Correct the grammar of the user's sentence. "
            "Reply with ONLY the corrected sentence, nothing else."},
            {"role": "user", "content": query},
        ],
        temperature=0,
    )
    corrected = response.choices[0].message.content.strip()
    return f"Corrected: {corrected}"


TOOL_ROUTES = {
    "math": math_tool,
    "python_help": python_help_tool,
    "english_grammar": english_grammar_tool,
}


def classify_intent(query: str) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
        temperature=0,
    )
    label = response.choices[0].message.content.strip()

    if label not in TOOL_ROUTES:
        print(f"  (Warning: unexpected label '{label}', defaulting to python_help)")
        label = "python_help"

    return label


def run_agent(query: str) -> str:
    print(f"\n[Observe] Query: {query}")

    tool_name = classify_intent(query)
    print(f"[Decide] Selected tool: {tool_name}")

    # Human-in-loop confirmation before acting
    confirm = input(f"  Proceed with '{tool_name}' tool? (y/n): ").strip().lower()
    if confirm != "y":
        print("[Act] Cancelled by user.")
        return "Cancelled"

    tool_function = TOOL_ROUTES[tool_name]

    # Error-safe tool invocation
    try:
        result = tool_function(query)
    except Exception as e:
        result = f"Tool failed unexpectedly: {e}"

    print(f"[Act] Tool response: {result}")
    return result


def main():
    print("Student Helper Agent")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Ask a question (math / python / grammar): ")
        if query.strip().lower() == "exit":
            print("Goodbye!")
            break
        run_agent(query)


if __name__ == "__main__":
    main()