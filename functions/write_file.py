import os
from google.genai import types


def write_file(working_dir, file_path, content):
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


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write the given content to a specified file within the working directory, if the file already exists it will be overwritten and the parent directories of the given relative file path will be created if it doesn't exist",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path of the file to be written. it should be relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the specifed file",
            ),
        },
    ),
)
