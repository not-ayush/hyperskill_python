# STAGE 2
import re
path = input()

with open(path, "r") as file:
    lines = [x[:-1] for x in file.readlines()]


class StyleChecks:
    checks_msg = {"S001": "S001 Too long",
                  "S002": "S002 Indentation is not a multiple of four",
                  "S003": "S003 Unnecessary semicolon",
                  "S004": "S004 At least two spaces required before inline comments",
                  "S005": "S005 TODO found",
                  "S006": "S006 More than two blank lines used before this line"
                  }

    @staticmethod
    def check_line_len(line_: str, n: int):
        if len(line_) > 79:
            return n+1, "S001"

    @staticmethod
    def check_indent(line_: str, n: int):
        count_spaces = 0
        for char in line_:
            if char.isspace():
                count_spaces += 1
            else:
                break
        if count_spaces % 4 != 0:
            return n+1, "S002"

    @staticmethod
    def check_semicolon(line_: str, n: int):
        code = re.search(r"(.*;)$|(.*;\s*#.*)", line_) and not re.search(r".*#.*;.*", line_)
        if bool(code):
            return n+1, "S003"

    @staticmethod
    def check_comment_spaces(line_: str, n: int):
        check = re.search(r'\s*#', line_) and not re.search(r'^#', line_)
        if check and len(re.search(r'\s*#', line_).group(0)) < 3:
            return n+1, "S004"

    @staticmethod
    def check_todo(line_: str, n: int):
        if re.search(r"\s*#.*?TODO", line_, re.IGNORECASE):
            return n+1, "S005"

    @staticmethod
    def check_blank_lines(line_: str, n: int):
        if n > 3 and all([lines[n-i] == '' for i in range(1, 4)]):
            return n+1, "S006"

    check_fxns = {check_line_len, check_indent, check_semicolon,
                  check_comment_spaces, check_todo, check_blank_lines}


checked = list()
for line_n, line in enumerate(lines):
    for check_fxn in StyleChecks.check_fxns:
        result = check_fxn(line, line_n)
        if result:
            checked.append(result)

checked.sort(key=lambda x: (x[0], int(x[1][1:])))

for checks in checked:
    print(f"Line {checks[0]}: {StyleChecks.checks_msg[checks[1]]}")

'''
loop through lines, call all style checks on each line. 
each stylecheck fxn returns truthy things if it is true, and that truthy thing is the 
key for its message dictionary
to loop through all styles as well, create a dictionary to store the style check fxns
only one call on each line right? 

loop through lines, on each line, call all functions, add the returned values to a set. 
print at the end. 
'''