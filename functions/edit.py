import os

from agent import agent
from pydantic_ai import RunContext
import difflib


@agent.tool
def edit(ctx: RunContext[str], file_path: str, old_string: str, new_string: str) -> str:
    """
    Replace an exact text block in a file.

    The file must be inside the working directory. The tool
    finds `old_string` and replaces it with `new_string`.
    For safety, `old_string` must appear exactly once in
    the file.

    Args:
        file_path: Path to the file to edit.
        old_string: Text to replace.
        new_string: Replacement text.

    Returns:
        A success message or an error message if the edit
        could not be applied.
    """
    working_dir = ctx.deps if type(ctx) is not str else ctx
    print(f"--calling edit({file_path}, {old_string}, {new_string})")
    if old_string == new_string:
        return "Error: old_string and new_string cannot be same"
    abs_path: str = os.path.abspath(working_dir)
    full_path: str = os.path.join(abs_path, file_path)
    target_path: str = os.path.normpath(full_path)

    try:
        valid_target: bool = os.path.commonpath([target_path, abs_path]) == abs_path
    except:
        valid_target = False

    if not valid_target:
        return f'Error: Cannot edit "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_path):
        return f'Error: Cannot edit "{file_path}" as it is a directory'
    content = ""
    new_content = ""
    with open(target_path, "r") as file:
        content = file.read()
        start = content.find(old_string)
        if content.count(old_string) > 1:
            return f"Error: The edit cannot be performed as more than one match of the {old_string} is found."
        if start == -1:
            return f"Error: The edit cannot be applied as the old_string: {old_string} is not found in {file_path}"
        end = start + len(old_string)

        new_content = content[:start] + new_string + content[end:]
    with open(target_path, "w") as file:
        file.write(new_content)
    diff = "\n".join(
        list(
            difflib.unified_diff(
                content.splitlines(),
                new_content.splitlines(),
                fromfile="before",
                tofile="after",
            )
        )
    )
    output = "EDIT Successfully applied\n" + diff
    print(output)
    return output
