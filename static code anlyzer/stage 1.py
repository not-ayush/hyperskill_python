# too long check stage 1

path = input()
longer = []

with open(path, "r") as file:
    for i, line in enumerate(file.readlines()):
        if len(line) > 79:
            longer.append(i)
    for i in longer:
        print(f"Line {i+1}: S001 Too long")
