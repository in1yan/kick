from distro import name
import os
import sys
import subprocess
from google.genai import types


def run_python_file(working_dir, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_dir)
        full_path = os.path.join(abs_path, file_path)
        target_file = os.path.normpath(full_path)

        try:
            valid_path = os.path.commonpath([target_file, abs_path]) == abs_path
        except:
            valid_path = False
        if not valid_path:
            return f'Error: Cannot run "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: Cannot run "{file_path}" as it is not a file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = [sys.executable, target_file]
        if args:
            command.extend(args)

        sb = subprocess.run(
            command, cwd=abs_path, timeout=30, text=True, capture_output=True
        )
        output = ""
        if sb.returncode != 0:
            output += f"Process exited with code {sb.returncode}\n"
        if not sb.stderr and not sb.stdout:
            output += "No output produced"
        output += "STDOUT:\n" + sb.stdout
        output += "STDERR:\n" + sb.stderr
        return output
    except Exception as e:
        return f"Error: executing python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the give python file and returns the stdout and stderr",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path of the file to be executed. it should be relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="The list of command line arguments needed by the give python file.",
            ),
        },
    ),
)
