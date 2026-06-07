# KICK - Coding Agent

Kick is an simple coding agent that uses pydantic ai. It can read, write, and edit code.
<img width="400" height="225" alt="Screen Recording 2026-05-18 184310" src="https://github.com/user-attachments/assets/11fa0c41-5fda-4f71-8c71-7724b3e7e604" />

## Features

- **File Operations**: Read, write, edit and list files in the workspace
- supports multiple providers

## Installation

1. Clone the repository
2. Install dependencies: `uv sync`
3. Set your api key:

 example:

   ```
   GEMINI_API_KEY=your_api_key_here
   ```
4. setup a model:

    example:
    ```

    MODEL=groq:openai/gpt-oss-120b   
    ```
    ```
## Usage

Run the agent with a prompt:

```bash
uv run main.py "Your prompt here"
```

Run the agent in multiturn conversation:

```bash
uv run main.py
```

## How It Works

The agent uses ai models to call several functions which will help the llm to interact with the file system.
- `read`: Read file contents
- `ls`: List files and directories
- `write`: Create or modify files
- `edit`: edit a file

> Note: This is a learning project with a simple implementation, Not recommended to use for serious stuff.
