from station import Station
import csv

def load_stations(input_file):
    stations = {}
    with open(input_file) as file:
        reader = csv.reader(file)
        next(reader)
        while True:
            line = file.readline()
            if line == "":
                break
            split = line.split(",")
            stations[split[0]] = Station((split[0]), float(split[1]), float(split[2]))
    return stations

def load_connections(input_file, stations):
    with open(input_file) as file:
        reader = csv.reader(file)
        next(reader)
        while True:
            line = file.readline()
            if line == "":
                break
            split = line.split(",")
            
            # Twee richtingen
            stations[split[0]].add_connection(split[1], int(split[2]))
            stations[split[1]].add_connection(split[0], int(split[2]))