import json
import re


class CheckData:
    def __init__(self, json_inp):
        self.json_inp = json_inp
        self.database = json.loads(json_inp)
        self.type_err_count = {"bus_id": 0, "stop_id": 0, "stop_name": 0,
                               "next_stop": 0, "stop_type": 0, "a_time": 0}
        self.format_err_count = {"stop_name": 0, "stop_type": 0, "a_time": 0}

    type_checks = {
        "bus_id": lambda x: x and isinstance(x, int),
        "stop_id": lambda x: x and isinstance(x, int),
        "stop_name": lambda x: x and isinstance(x, str),
        "next_stop": lambda x: x is not None and isinstance(x, int),
        "stop_type": lambda x: isinstance(x, str) and len(x) <= 1,
        "a_time": lambda x: x and isinstance(x, str),
    }

    regex = (re.compile(r'(?:[A-Z][a-z]+ )+?(?=Street$|Boulevard$|Avenue$|Road$)'),
             re.compile(r'^[SOF]$'), re.compile(r'([01]\d|2[0-3]):[0-5]\d$'))

    format_checks = {
        "stop_name": lambda x: bool(re.match(CheckData.regex[0], x)),
        "stop_type": lambda x: True if x == '' else bool(re.match(CheckData.regex[1], x)),
        "a_time": lambda x: bool(re.match(CheckData.regex[2], x))
    }

    def type_ok(self):
        for entry in self.database:
            for field, value in entry.items():
                if not self.type_checks[field](value):
                    self.type_err_count[field] += 1
        error_sum = sum(list(self.type_err_count.values()))
        print(f"Type and required field validatoin: {error_sum} errors")
        for field, value in self.type_checks.items():
            print(f"{field}: {self.type_err_count[field]}")

    def format_ok(self):
        for entry in self.database:
            for field, value in entry.items():
                # if field == "stop_type" and value not in 'SOF': print(field, value, self.format_checks[field](value))
                if (field in CheckData.format_checks.keys()) and (not self.format_checks[field](value)):
                    self.format_err_count[field] += 1
        error_sum = sum(list(self.format_err_count.values()))
        print(f"Format validation: {error_sum} errors")
        for field in self.format_checks.keys():
            print(f"{field}: {self.format_err_count[field]}")


data_check = CheckData(input())
data_check.format_ok()
