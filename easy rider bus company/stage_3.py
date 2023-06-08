import json


class CheckData:
    def __init__(self, json_inp):
        self.json_inp = json_inp
        self.database = json.loads(json_inp)
        self.stop_count = dict()

    def line_number_ok(self):
        for entry in self.database:
            line_n = entry["bus_id"]
            if self.stop_count.get(line_n) is None:
                self.stop_count.update({line_n: 1})
            else:
                self.stop_count[line_n] += 1

        print("Line names and number of stops:")
        for line_n, count in self.stop_count.items():
            print(f"bus_id: {line_n}, stops: {count}")


CheckData(input()).line_number_ok()
