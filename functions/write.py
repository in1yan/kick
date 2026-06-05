import os
from agent import agent
from pydantic_ai import RunContext


@agent.tool
def write(ctx: RunContext[str], file_path, content):
    """
    Write content to a file in the workspace, creating parent directories if needed.

    Args:
        file_path: Path to the file relative to the workspace.
        content: Text to write to the file.

    Returns:
        A success message or an error message.
    """
    working_dir = ctx.deps
    print(f"--calling write({working_dir}, {file_path}, {content})")
    try:
        abs_path = os.path.abspath(working_dir)
        full_path = os.path.join(abs_path, file_path)
        target_path = os.path.normpath(full_path)

        try:
            valid_target = os.path.commonpath([target_path, abs_path]) == abs_path
        except:
            valid_target = False

        if not valid_target:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        parent_dir = os.path.dirname(target_path)

        os.makedirs(parent_dir, exist_ok=True)
        with open(target_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except:
        return f'Error: Cannot write to "{file_path}"'
