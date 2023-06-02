import re
import os
import argparse

parser = argparse.ArgumentParser(description='print file style errors')
parser.add_argument('path', help='enter a file or directory path')
args = parser.parse_args()
path = args.path
lines = []


class StyleChecks:
    """
    store functions to check style errors in a line
    each function takes a line (str) argument, and a line number (int) argument
    functions return the line number and message if style error is found
    """

    @staticmethod
    def check_line_len(line_: str, n: int):
        if len(line_) > 79:
            return n+1, "S001 Too long"

    @staticmethod
    def check_indent(line_: str, n: int):
        count_spaces = 0
        for char in line_:
            if char.isspace():
                count_spaces += 1
            else:
                break
        if count_spaces % 4 != 0:
            return n+1, "S002 Indentation is not a multiple of four"

    @staticmethod
    def check_semicolon(line_: str, n: int):
        code = re.search(r"(.*;)$|(.*;\s*#.*)", line_) and not re.search(r".*#.*;.*", line_)
        if bool(code):
            return n+1, "S003 Unnecessary semicolon"

    @staticmethod
    def check_comment_spaces(line_: str, n: int):
        check = re.search(r'\s*#', line_) and not re.search(r'^#', line_)
        if check and len(re.search(r'\s*#', line_).group(0)) < 3:
            return n+1, "S004 At least two spaces required before inline comments"

    @staticmethod
    def check_todo(line_: str, n: int):
        if re.search(r"\s*#.*?TODO", line_, re.IGNORECASE):
            return n+1, "S005 TODO found"

    @staticmethod
    def check_blank_lines(line_: str, n: int):
        if n > 3 and all([lines[n-i] == '' for i in range(1, 4)]):
            return n+1, "S006 More than two blank lines used before this line"

    # name checking fxns: check if applicable line, if not correctly named, return message

    @staticmethod
    def check_construct_space(line_n: str, n: int):
        if line_n.lstrip().startswith('class') or line_n.lstrip().startswith('def'):
            match = re.search(r'(def|class)\s\w+', line_n)
            if match is None:
                construct_name = re.search(r'(def|class)\s+\w+', line_n).group(1)
                return n+1, f"S007 Too many space after '{construct_name}'"

    @staticmethod
    def check_class_name(line_n: str, n: int):
        if line_n.lstrip().startswith('class'):
            match = re.search(r'class\s+((?:[A-Z][a-z]+)+)', line_n)
            if match is None:
                class_name = re.search(r'class\s+(\w+)', line_n).group(1)
                return n+1, f"S008 Class name '{class_name}' should use CamelCase"

    @staticmethod
    def check_func_name(line_n: str, n: int):
        if line_n.lstrip().startswith('def'):
            match = re.search(r'def\s+([a-z_]+)', line_n)
            if match is None:
                func_name = re.search(r'def\s+(\w+)', line_n).group(1)
                return n+1, f"S009 Function name '{func_name}' should use snake_case"

    check_fxns = [check_line_len, check_indent, check_semicolon,
                  check_comment_spaces, check_todo, check_blank_lines,
                  check_construct_space, check_class_name, check_func_name]


def check_file(file_path: str):
    """checks all the style errors for given file
     and prints them, argument is file path"""
    global lines
    with open(file_path, "r") as file:
        lines = [x[:-1] for x in file.readlines()]

    messages_set = set()
    for line_n, line in enumerate(lines):
        for check_fxn in StyleChecks.check_fxns:
            result = check_fxn(line, line_n)
            if result:
                messages_set.add(result)

    # sort the messages by first line number, second error code
    messages = sorted(list(messages_set), key=lambda x: (x[0], int(x[1][1:4])))
    for message in messages:
        print(f"{file_path}: Line {message[0]}: {message[1]}")


def get_files(path_: str):
    """return a list of .py files path in given directory and all subfolders"""
    files_lst = []
    for i in os.listdir(path_):
        current = os.path.join(path_, i)
        if current.endswith('tests.py'):
            continue
        elif os.path.isfile(current) and current.endswith('.py'):
            files_lst.append(current)
        elif os.path.isdir(current):
            files_lst.extend(get_files(current))
    return files_lst


if os.path.isfile(path):
    check_file(path)
else:
    files = get_files(path)
    files.sort()
    for f in files:
        check_file(f)