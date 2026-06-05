from get_file_content import get_file_content

print(get_file_content("../examples/calculator", "lorem.txt"))
print(get_file_content("../examples/calculator", "main.py"))
print(get_file_content("../examples/calculator", "pkg/calculator.py"))
print(get_file_content("../examples/calculator", "/bin/cat"))
print(get_file_content("../examples/calculator", "pkg/not_found.py"))
