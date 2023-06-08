import json


class CheckData:
    def __init__(self, json_inp):
        self.json_inp = json_inp
        self.database = json.loads(json_inp)

    def arrival_time_ok(self):
        error = []
        # data = self.database.sort(key= lambda x: (x["bus_id"], x["stop_id"]))
        line_to_skip = []
        for i, entry in enumerate(self.database):
            this_stop, this_time, line_n = entry["stop_name"], entry["a_time"], entry["bus_id"]
            if i > 0  and (self.database[i - 1]["bus_id"] == line_n) and (line_n not in line_to_skip):
                if self.database[i - 1]["a_time"] > this_time:
                    error.append((line_n, this_stop))
                    line_to_skip.append(line_n)
                    continue
        if error:
            print("Arrival time test:")
            for i in error:
                print(f"bus_id line {i[0]}: wrong time on station {i[1]}")
        else: print("Arrival time test:\nOK")

CheckData(input()).arrival_time_ok()

'''
Check that the arrival time for the upcoming stops for a given bus line is increasing.
If the arrival time for the next stop is earlier than or equal to the time of the current stop, 
stop checking that bus line and remember the name of the incorrect stop.
Display the information for those bus lines that have time anomalies. For the correct stops, do not display anything.
If all the lines are correct timewise, print OK.
Arrival time test:
bus_id line 128: wrong time on station Fifth Avenue
bus_id line 256: wrong time on station Sunset Boulevard
Arrival time test:
OK
'''
'''
store = {line: [(time1, stop1), (time2, stop2)...], ...}
wrong = {line: [(time1, stop1), (time2, stop2)...], ...}
loop through the database:
    if the current bus line has not been enccounctered yet ie. does not exist in stored values, 
        store it and initiate its arrival time list with the current stop
    else:  # when the bus line list has been initiated in dictionary
        if the time of the last element of the list is more than the current.
            store it in the "wrong" dict
'''