import ast
import re
import os
import argparse

parser = argparse.ArgumentParser(description='print file style errors')
parser.add_argument('path', help='enter a file or directory path')
args = parser.parse_args()
path = args.path
lines = []


class LineChecks:
    """
    store functions to check style errors in a line
    each function takes a line (str) argument, and a line number (int) argument
    functions return the line number and message if style error is found
    """

    @staticmethod
    def check_line_len(line: str, n: int):
        if len(line) > 79:
            return n+1, "S001 Too long"

    @staticmethod
    def check_indent(line: str, n: int):
        count_spaces = 0
        for char in line:
            if char.isspace():
                count_spaces += 1
            else:
                break
        if count_spaces % 4 != 0:
            return n+1, "S002 Indentation is not a multiple of four"

    @staticmethod
    def check_semicolon(line: str, n: int):
        code = re.search(r"(.*;)$|(.*;\s*#.*)", line) and not re.search(r".*#.*;.*", line)
        if bool(code):
            return n+1, "S003 Unnecessary semicolon"

    @staticmethod
    def check_comment_spaces(line: str, n: int):
        check = re.search(r'\s*#', line) and not re.search(r'^#', line)
        if check and len(re.search(r'\s*#', line).group(0)) < 3:
            return n+1, "S004 At least two spaces required before inline comments"

    @staticmethod
    def check_todo(line: str, n: int):
        if re.search(r"\s*#.*?TODO", line, re.IGNORECASE):
            return n+1, "S005 TODO found"

    @staticmethod
    def check_blank_lines(_line: str, n: int):
        if n > 3 and all([lines[n-i] == '' for i in range(1, 4)]):
            return n+1, "S006 More than two blank lines used before this line"

    # name checking fxns: check if applicable line, if not correctly named, return message

    @staticmethod
    def check_construct_space(line: str, n: int):
        if line.lstrip().startswith('class') or line.lstrip().startswith('def'):
            match = re.search(r'(def|class)\s\w+', line)
            if match is None:
                construct_name = re.search(r'(def|class)\s+\w+', line).group(1)
                return n+1, f"S007 Too many space after '{construct_name}'"

    @staticmethod
    def check_class_name(line: str, n: int):
        if line.lstrip().startswith('class'):
            match = re.search(r'class\s+((?:[A-Z][a-z]+)+)', line)
            if match is None:
                class_name = re.search(r'class\s+(\w+)', line).group(1)
                return n+1, f"S008 Class name '{class_name}' should use CamelCase"

    @staticmethod
    def check_func_name(line: str, n: int):
        if line.lstrip().startswith('def'):
            match = re.search(r'def\s+([a-z_]+)', line)
            if match is None:
                func_name = re.search(r'def\s+(\w+)', line).group(1)
                return n+1, f"S009 Function name '{func_name}' should use snake_case"

    check_fxns = (check_line_len, check_indent, check_semicolon,
                  check_comment_spaces, check_todo, check_blank_lines,
                  check_construct_space, check_class_name, check_func_name)


class FileChecks:
    """these functions use AST module to check for style errors in the whole file at once,
    AST object is the argument, set of tuples containing line no and message is returned
    """

    @staticmethod
    def check_arg_name(t: ast.parse):
        errors = set()
        for func in [n for n in ast.walk(t) if isinstance(n, ast.FunctionDef)]:
            for i in func.args.args:
                arg_name = i.arg
                if re.match(r'[a-z_]+', arg_name):
                    pass
                else:
                    errors.add((i.lineno, f"S010 Argument name {arg_name} should be written in snake_case"))
        return errors

    @staticmethod
    def check_var_name(t: ast.parse):
        errors = set()
        for n in ast.walk(t):
            if isinstance(n, ast.Assign):
                try: var_name, line_n = n.targets[0].id, n.targets[0].lineno
                except AttributeError: pass
                else:
                    if re.match(r'[a-z_]+', var_name): pass
                    else:
                        errors.add((line_n, f"S011 Variable name '{var_name}' should be written in snake_case"))
        return errors

    @staticmethod
    def check_arg_mutable(t: ast.parse):
        errors = set()
        for node in ast.walk(t):
            if isinstance(node, ast.FunctionDef):
                if any([isinstance(t, (ast.List, ast.Set, ast.Dict)) for t in node.args.defaults]):
                    errors.add((node.lineno, f"S012 The default argument value is mutable"))
        return errors

    check_fxns = (check_arg_name, check_var_name, check_arg_mutable)


def check_file(file_path: str):
    """checks all the style errors for given file
     and prints them, argument is file path"""
    global lines
    with open(file_path, "r") as file:
        lines = [x[:-1] for x in file.readlines()]
        file.seek(0)
        tree = ast.parse(file.read())

    messages_set = set()
    for line_n, line in enumerate(lines):
        for check_fxn in LineChecks.check_fxns:
            result = check_fxn(line, line_n)
            if result:
                messages_set.add(result)
    for check_fxn in FileChecks.check_fxns:
        result = check_fxn(tree)
        if result:
            messages_set.update(result)

    # sort the messages by first line number, second error code
    messages = sorted(list(messages_set), key=lambda x: (x[0], int(x[1][1:4])))
    for message in messages:
        print(f"{file_path}: Line {message[0]}: {message[1]}")


def get_files(dir_path: str):
    """return a list of .py files path in given directory and all subfolders"""
    files_lst = []
    for i in os.listdir(dir_path):
        current = os.path.join(dir_path, i)
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
