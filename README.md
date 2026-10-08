# Student Helper Agent

A Python-based student helper agent that classifies user queries and
automatically routes them to the appropriate tool.

## Features

- Classifies student queries into three categories:
  - Math
  - Python Help
  - English Grammar
- Routes each query to the appropriate tool.
- Human-in-the-loop confirmation before tool execution.
- Safe arithmetic evaluation.
- Provides basic Python programming guidance.
- Uses Groq LLM for query classification and English grammar correction.
- Includes error-safe tool invocation.

## Technologies Used

- Python
- Groq API
- python-dotenv
- Regular Expressions

## How It Works

1. The user enters a query.
2. The Groq LLM classifies the query as:
   - `math`
   - `python_help`
   - `english_grammar`
3. The system selects the corresponding tool.
4. The user confirms whether the tool should execute.
5. The selected tool processes the query.
6. The result is displayed to the user.

## Example

### Math

User:
What is 25 * 4?

The agent identifies the query as:

`math`

and routes it to the math tool.

### Python Help

User:
How do I create a list in Python?

The agent identifies the query as:

`python_help`

and provides a basic explanation.

### English Grammar

User:
She go to college every day.

The agent identifies the query as:

`english_grammar`

and uses the Groq LLM to correct the sentence.

## Installation

Clone the repository:

```bash
git clone https://github.com/Bhavanisri25/student-helper-agent.git
cd student-helper-agent
