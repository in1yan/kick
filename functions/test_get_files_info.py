from get_files_info import get_files_info

print(get_files_info("../examples/calculator", "."))
print(get_files_info("../examples/calculator", "/bin"))
print(get_files_info("../examples/calculator", "../"))
print(get_files_info("../examples/calculator", "main.py"))
print(get_files_info("../examples/calculator", "pkg"))
