from read import read

print(read("../examples/calculator", "lorem.txt"))
print(read("../examples/calculator", "main.py"))
print(read("../examples/calculator", "pkg/calculator.py"))
print(read("../examples/calculator", "/bin/cat"))
print(read("../examples/calculator", "pkg/not_found.py"))
