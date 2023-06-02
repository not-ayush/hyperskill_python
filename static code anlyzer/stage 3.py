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
    store style messages and functions to check style errors in a line
    each function takes a line (str) argument, and a line number (int) argument
    """
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


def check_file(file_path: str):
    """checks all the style errors for given file
     and prints them, argument is file path"""
    global lines
    with open(file_path, "r") as file:
        lines = [x[:-1] for x in file.readlines()]

    checked = list()
    for line_n, line in enumerate(lines):
        for check_fxn in StyleChecks.check_fxns:
            result = check_fxn(line, line_n)
            if result:
                checked.append(result)
    checked.sort(key=lambda x: (x[0], int(x[1][1:])))

    for checks in checked:
        print(f"{file_path}: Line {checks[0]}: {StyleChecks.checks_msg[checks[1]]}")


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


'''
stage 3:
    commandline input
    accept file_path or folder_path
    Path: Line X: Code Message 
    output lines sorted in order of file name
    non python files skipped.
    all previous things apply, 
        one line same issue twice but print once, 
        false positives in strings can are ok
        
/path/to/project/script2.py: Line 1: S004 At least two spaces required before inline comments
/path/to/project/script2.py: Line 3: S001 Too long line
/path/to/project/somedir/script.py: Line 3: S001 Too long line
/path/to/project/test.py: Line 3: Line 13: S003 Unnecessary semicolon

pseudo pseudo code:
    ask path, 
    if file:
        do the same as stage 2, just change the error message
    if direcotry:
        store the file paths in list, 
        remove non python file paths, 
        sort the list acc to file name
        loop through path list:
            do the same as stage 2 for file, jsut change the error message
            
    the loop through the path given has to be 
    recursive to get the paths of all files in all subfolders
    loop through listdir:
        if file, add it to list
        if folder, call the function recursively on this folder.
'''
