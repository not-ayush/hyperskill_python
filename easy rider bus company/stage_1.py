import json

json_inp = input()
database = json.loads(json_inp)

"""dictionary where key,value pair is (<field>: [<check_valid_type()>, <error_count: int>])
functions called by basic_checks[<field>][0](value_to_check)"""
basic_checks = {
    "bus_id": [lambda x: x and isinstance(x, int), 0],
    "stop_id": [lambda x: x and isinstance(x, int), 0],
    "stop_name": [lambda x: x and isinstance(x, str), 0],
    "next_stop": [lambda x: x is not None and isinstance(x, int), 0],
    "stop_type": [lambda x: isinstance(x, str) and len(x) <= 1, 0],
    "a_time": [lambda x: x and isinstance(x, str), 0],
}

for entry in database:
    for field, value in entry.items():
        if not basic_checks[field][0](value):
            basic_checks[field][1] += 1

error_count = sum([x[1] for x in list(basic_checks.values())])
print(f"Type and required field validatoin: {error_count} errors")
for field, value in basic_checks.items():
    print(f"{field}: {value[1]}")