import os

# from config import Config
from google.genai import types

MAX_CHARS = 10000


def get_file_content(working_dir, file_path):
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


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the content of the file within the working directory , the output will be terminated if the file size is large",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path of the file to be read. it should be relative to the working directory.",
            )
        },
        required=["file_path"],
    ),
)
