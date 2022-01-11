from station import Station


def load_stations(input_file):
    with open(input_file, 'r') as file:
        # Skip header line
        next(file)
        
        stationlist = []
        
        for line in file:
            stationlist.append(line.strip().split(","))
            
        # Add station information to dictionary        
        stations = {x[0]: Station(x[0], float(x[1]), float(x[2])) for x in stationlist}

    return stations


def load_connections(input_file, stations):
    with open(input_file, 'r') as file:
        # Skip header line
        next(file)
        
        connectionlist = []
        
        for line in file:
            connectionlist.append(line.strip().split(","))
            
        # Add connections to stations            
        for x in connectionlist:
            stations[x[0]].add_connection(x[1], int(x[2]))
            stations[x[1]].add_connection(x[0], int(x[2]))
