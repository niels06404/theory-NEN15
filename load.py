from station import Station


def load_stations(input_file):
    with open(input_file, 'r') as file:
        # Skip header line
        next(file)
        
        # Add station information to dictionary
        stations = {}
        
        for line in file:
            x = line.strip().split(',')
            stations[x[0]] = Station(x[0], float(x[1]), float(x[2]))

    return stations

def load_connections(input_file, stations):
    with open(input_file, 'r') as file:
        # Skip header line
        next(file)
        
        # Add connections to stations  
        for line in file:
            x = line.strip().split(',')

            # add connection with time
            stations[x[0]].add_connection(x[1], float(x[2]))
            stations[x[1]].add_connection(x[0], float(x[2]))

            # add connection with coordinates
            stations[x[0]].add_connection_loc(x[1], stations[x[1]]._x, stations[x[1]]._y)
            stations[x[1]].add_connection_loc(x[0], stations[x[0]]._x, stations[x[0]]._y)