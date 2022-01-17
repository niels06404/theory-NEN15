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
        connections_all = set()
        with open(input_file, 'r') as file:
            # Skip header line
            next(file)

            # Add connections to stations
            for line in file:
                x = line.strip().split(',')

                # Add connections to Station class
                self.stations[x[0]].add_connection(x[1], float(x[2]))
                self.stations[x[1]].add_connection(x[0], float(x[2]))

                # Save a set of all connections
                # NOTE: hier kunnen we nog tellen hoe vaak connectie gebruikt
                connections_all.add((x[0], x[1]))
                connections_all.add((x[1], x[0]))
        
        return connections_all

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

        connections_inversed = set()
        for connection in connections:
            connections_inversed.add((connection[1], connection[0]))

        connections = connections.union(connections_inversed)

        return connections
    
    def get_unused_connections(self):
        return list(self.connections - self.get_visited_connections())

    def calculate_score(self):
        '''
        Calculates the score of the result bases on a given formula: K = p * 10000 - (T * 100 + Min).
        In which K is the quality of the generated routes, p the fraction of the used connections, T the number of routes and
        Min the total time of all routes (in minutes).
        '''
        # 56 for Holland, 178 for Nationaal - I think
        p = len(self.get_visited_connections()) / len(self.connections)
        t = len(self.routes)
        m = 0
        for route in self.routes:
            m += self.routes[route].time

        score = p * 10000 - (t * 100 + m)
        return score
