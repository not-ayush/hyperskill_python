import json


class CheckData:
    def __init__(self, json_inp):
        self.json_inp = json_inp
        self.database = json.loads(json_inp)

    def get_transfer_stops(self):
        transfer = []
        store = []  # [(stop_name, bus_line),...]
        for entry in self.database:
            this_name, this_line = entry["stop_name"], entry["bus_id"]
            if store and any([(x[0] == this_name) and (x[1] != this_line) for x in store]) \
                    and this_name not in transfer:
                transfer.append(this_name)
                continue
            store.append((this_name, this_line))
        return transfer

    def get_all_stops(self):
        store = {"S": [], "T": [], "F": [], "O": []}
        for entry in self.database:
            this_stop, this_name, this_line = entry["stop_type"], entry["stop_name"], entry["bus_id"]
            if (this_stop and this_stop in "SOF") and this_name not in store[this_stop]:
                store[this_stop].append(this_name)
        store["T"] = self.get_transfer_stops()
        return store

    def on_demond_ok(self):
        stops = self.get_all_stops()
        s, f, t, o = set(stops["S"]), set(stops["F"]), set(stops["T"]), set(stops["O"])
        wrong_stops = (o & t) | (o & s) | (o & f)
        print("On demand stops test:")
        if wrong_stops:
            print("Wrong stop type:", sorted(list(wrong_stops)))
        else: print("OK")


CheckData(input()).on_demond_ok()
