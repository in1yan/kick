import os


def get_files_info(working_dir, dir="."):
    abs_path = os.path.abspath(working_dir)
    full_path = os.path.join(abs_path, dir)
    target_dir = os.path.normpath(full_path)
    try:
        valid_target_dir = os.path.commonpath([target_dir, abs_path]) == abs_path
    except ValueError:
        valid_target_dir = False
    if not valid_target_dir:
        return f'Error: Cannot list "{dir}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: directory "{dir}" is not a directory'

    file_info = [f"Result for {dir if dir != '.' else 'current'} directory:"]

    contents = os.listdir(target_dir)
    for content in contents:
        content_path = os.path.join(target_dir, content)
        file_info.append(
            f"- {content}: file_size = {os.path.getsize(content_path)} bytes , is_dir = {os.path.isdir(content_path)}"
        )
    return "\n".join(file_info)


if __name__ == "__main__":
    print(get_files_info("../examples", dir="."))
