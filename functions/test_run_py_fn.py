from run_python_file import run_python_file

print(run_python_file("../examples/calculator", "main.py"))
print(run_python_file("../examples/calculator", "main.py", ["2 + 5"]))
print(run_python_file("../examples/calculator", "tests.py"))
print(run_python_file("../examples/calculator", "notfound.py"))
print(run_python_file("../examples/calculator", "lorem.txt"))
