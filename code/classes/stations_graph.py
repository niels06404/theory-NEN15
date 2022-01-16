from .station import Station
from .route import Route


class StationsGraph():
    def __init__(self, stations_file, connections_file):
        self.stations = self.load_stations(stations_file)
        self.connections = self.load_connections(connections_file)
        self.routes = {}

    def load_stations(self, input_file):
        '''
        Loads all the stations into the graph.
        '''
        with open(input_file, 'r') as file:
            # Skip header line
            next(file)

            # Add station information to dictionary
            stations = {}

            for line in file:
                x = line.strip().split(',')
                stations[x[0]] = Station(x[0], float(x[1]), float(x[2]))

        return stations

    def load_connections(self, input_file):
        '''
        Loads all the connections into the stations.
        '''
        with open(input_file, 'r') as file:
            # Skip header line
            next(file)

            # Add connections to stations
            for line in file:
                x = line.strip().split(',')

                # Add connection with time
                self.stations[x[0]].add_connection(x[1], float(x[2]))
                self.stations[x[1]].add_connection(x[0], float(x[2]))

                # Add connection with coordinates
                self.stations[x[0]].add_connection_loc(x[1], self.stations[x[1]]._x, self.stations[x[1]]._y)
                self.stations[x[1]].add_connection_loc(x[0], self.stations[x[0]]._x, self.stations[x[0]]._y)

    def add_route(self, starting_station):
        '''
        Creates a new route with the given starting station.
        '''
        self.routes[starting_station._name] = Route(starting_station)

    def get_visited_connections(self):
        '''
        Returns a set of all made connections for all the routes.
        '''
        connections = set()
        for route in self.routes:
            connections = connections.union(self.routes[route].connections)

        duplicates = set()
        for connection in connections:
            duplicates.add((connection[1], connection[0]))

        connections = connections.union(duplicates)

        return connections

    def calculate_score(self):
        '''
        Calculates the score of the result bases on a given formula: K = p * 10000 - (T * 100 + Min).
        In which K is the quality of the generated routes, p the fraction of the used connections, T the number of routes and
        Min the total time of all routes (in minutes).
        '''
        # 56 for Holland, 178 for Nationaal - I think
        p = len(self.get_visited_connections()) / 56
        t = len(self.routes)
        m = 0
        for route in self.routes:
            m += self.routes[route].time

        score = p * 10000 - (t * 100 + m)
        return score
