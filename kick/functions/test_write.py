from write_file import write_file

print(write_file("../examples/calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print(
    write_file(
        "../examples/calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
    )
)
print(
    write_file(
        "../examples/calculator", "pkg/test/morelorem.txt", "lorem ipsum dolor sit amet"
    )
)
print(
    write_file("../examples/calculator", "/tmp/temp.txt", "this should not be allowed")
)
