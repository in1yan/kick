import os
from agent import agent
from pydantic_ai import RunContext

MAX_CHARS = 10000


@agent.tool
def read(ctx: RunContext[str], file_path: str) -> str:
    """
    Read the contents of a file in the project workspace.

    Use this tool when you need to inspect source code, configuration files,
    logs, or other project files. The file path must be relative to the
    workspace root. Files outside the workspace cannot be accessed.

    Args:
        working_dir: Absolute path to the workspace root.
        file_path: Relative path of the file to read.

    Returns:
        The file contents as text. Large files may be truncated. Returns an
        error message if the file does not exist, is not a regular file, is
        outside the workspace, or cannot be read.
    """
    working_dir = ctx.deps

    print(f"--calling get_file_content({working_dir}, {file_path})")
    try:
        abs_path = os.path.abspath(working_dir)
        full_path = os.path.join(abs_path, file_path)
        target_file = os.path.normpath(full_path)

        try:
            valid_target_file = os.path.commonpath([target_file, abs_path]) == abs_path
        except ValueError:
            valid_target_file = False
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: file "{file_path}" is not a file'
        content = ""
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return content
    except Exception:
        return "Error: Cannot open or read the file"
