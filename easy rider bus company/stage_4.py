import json

class CheckData:
    def __init__(self, json_inp):
        self.json_inp = json_inp
        self.database = json.loads(json_inp)

    def line_paths_ok(self):
        lines = {}  # list has elements in this order: [s_count, f_count]
        for entry in self.database:
            this_type, this_line = entry["stop_type"], entry["bus_id"]
            if lines.get(this_line) is None:
                lines[this_line] = [0, 0]
            if this_type == "S" or this_type == "F":
                lines[this_line][0 if this_type == "S" else 1] += 1
        for line, count in lines.items():
            if not (count[0] == 1 and count[1] == 1):
                print(f"There is no start or end stop for the line: {line}")
                return
        return True

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

    def count_stops(self):
        store = {"S": [], "T": [], "F": []}
        for entry in self.database:
            this_stop, this_name, this_line = entry["stop_type"], entry["stop_name"], entry["bus_id"]
            # terminal
            if (this_stop == "S" or this_stop == "F") and this_name not in store[this_stop]:
                store[this_stop].append(this_name)
        store["T"] = self.get_transfer_stops()
        return store

    def check_stops(self):
        if not self.line_paths_ok(): return
        counted = self.count_stops()
        print("Start stops:", len(counted["S"]), sorted(counted["S"]))
        print("Transfer stops:", len(counted["T"]), sorted(counted["T"]))
        print("Finish stops:", len(counted["F"]), sorted(counted["F"]))


CheckData(input()).check_stops()

'''
make sure each bus line has exactly one S, and one F
If any busline does not meet this conndition, 
    stop checking further and print a message about this bus line. DOn't check others

if all bus lines meet the condition
    count how many starting points and final points each bus line has
    then print them in alphabetical order of their names (stop name)
    print transfer stop counts and their names in alphabetical order
----------

One function has to check the condition:
store  = {<line number>: [<s_found: bool>, <f_found: bool>]} default value instead of bool is None
for entry in database:
     if entry_stop_type is S or F:
        if this entry is in store already and its count for entry_stop_type is True:
            print( wrong shit ro whatever)
            stop the whole program
        if this entry doesn't exist:
            create it and update the appropriate counter, set other to None
if all lines have both S and F and exactly one S or F for one line in the entire database: pass
else: print( wrong shit message); stop the program
    
for entry in database:
    check stop type if S, F, or empty string
    update appropriate counter and list
print( good shit )
------- again

task: print the counts and list of names of each type of stop
"S", "F" is straight forward.
first we need to see if corrent stop_name is a transfer one or not
    a transfer stop_name is one that is shared by at least two bus lines.
    if the current stop type isn't S or F:
        in the entries you already looped over, 
            if there is one with the same stop name but different bus line
                then the current stop name is transfer line so, add it to transfer list



--------------- again
input: database
output: print counts of each type of stop, and list of names of each type of database

ptr:
    transfer stop is a stop shared by two lines
    if a stop name occurs multiple times as the same type it is counted as one
    names printed in alphatetical order

check transfer stops:
    transfer = []
    store = [(stop names, bus lines),...]
    loop through database:
        if stop name already exists and bus line is different than current bus line
            add current stop name to transer
            continue
        add current (stop_name, bus line) to store
    return transfer stops

store = dict(stop type: [(stop name, stop line), ...]
loop through database:
    if S or F (assume S for example):
        if the list corresponding to S has the same stop name already: 
            continue
        add (stop_name, stop_line) to S
        continue
store["T"] = check transfer stops()

'''
