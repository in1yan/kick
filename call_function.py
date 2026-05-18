from functions.write_file import schema_write_file, write_file
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.run_python_file import schema_run_python_file, run_python_file
from os import getcwd
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_write_file,
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
    ]
)


function_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(function_call, verbose=False):
    if verbose:
        print(f"- calling {function_call.name}({function_call.args})")
    print(f"- calling {function_call.name}")

    function_name = function_call.name or ""

    if function_call.name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    args = dict(function_call.args) if function_call.args else {}
    args["working_dir"] = getcwd()
    result = function_map[function_call.name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )
