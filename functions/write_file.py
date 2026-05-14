import os


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
