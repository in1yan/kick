# KICK - Coding Agent

Kick is an simple coding agent that uses Google's Gemini. It can read, write, and run code.

## Features

- **File Operations**: Read, write, and get information about files in the workspace
- **Code Execution**: Run Python files and see their output
- Supports verbose output to see the agent's token usage and tools calls.

It currently supports prompting thourgh command line args, so only single turn instructions can be given.
- Yet to implement a tui for multi turn converstion support.

## Installation

1. Clone the repository
2. Install dependencies: `uv sync`
3. Set your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

Run the agent with a prompt:

```bash
uv run main.py "Your prompt here"
```

For verbose output to see function calls and token usage:

```bash
uv run main.py "Your prompt here" --verbose
```

## How It Works

The agent uses gemini models to call several functions which will help the llm to interact with the file system.
- `get_file_content`: Read file contents
- `get_files_info`: List files and directories
- `write_file`: Create or modify files
- `run_python_file`: Execute Python scripts

> Note: This is a learning project with a simple implementation, Not recommended to use for serious stuff.