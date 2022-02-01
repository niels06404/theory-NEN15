import uuid

from .route import Route
from .station import Station


class StationsGraph():
    def __init__(self, stations_file: str, connections_file: str):
        self.stations = self.load_stations(stations_file)
        self.connections = self.load_connections(connections_file)
        self.routes: dict[str, Route] = {}

    def load_stations(self, input_file: str) -> dict:
        '''
        Loads all the stations into the graph.
        '''
        with open(input_file, "r") as file:
            # Skip header line
            next(file)

            stations = {}

            # Add station information to dictionary
            for line in file:
                x = line.strip().split(",")
                stations[x[0]] = Station(x[0], float(x[1]), float(x[2]))

        return stations

    def load_connections(self, input_file: str) -> dict:
        '''
        Loads all the connections into the stations.
        '''
        connections_all = {}
        with open(input_file, "r") as file:
            # Skip header line
            next(file)

            # Add connections to stations
            for line in file:
                x = line.strip().split(",")

                # Add connections to Station class
                self.stations[x[0]].add_connection(x[1], float(x[2]))
                self.stations[x[1]].add_connection(x[0], float(x[2]))

                # Save a set of all connections
                connections_all[((x[0], x[1]))] = 0
                connections_all[((x[1], x[0]))] = 0

        return connections_all

    def is_solution(self, the_map: str) -> bool:
        '''
        Returns True if the graph is a possible solution. False otherwise.
        '''
        if the_map == "Nationaal":
            if len(self.routes) > 20 or len([self.routes[x].time for x in self.routes if self.routes[x].time > 180]) > 0:
                return False
        elif the_map == "Holland":
            if len(self.routes) > 7 or len([self.routes[x].time for x in self.routes if self.routes[x].time > 120]) > 0:
                return False

        if len(self.routes) == 0:
            return False

        return True

    def add_route(self, starting_station: Station):
        '''
        Creates a new route with the given starting station.
        '''
        if starting_station._name not in self.routes.keys():
            self.routes[starting_station._name] = Route(starting_station)
        else:
            self.routes[starting_station._name + f"{uuid.uuid1()}"] = Route(starting_station)

    def get_visited_connections(self) -> set:
        '''
        Returns a set of all made connections for all the routes.
        '''
        connections: set[tuple[str, str]] = set()
        for route in self.routes:
            connections = connections.union(self.routes[route].connections)

        connections_inversed = set()
        for connection in connections:
            connections_inversed.add((connection[1], connection[0]))

        connections = connections.union(connections_inversed)

        return connections

    def get_unused_connections(self) -> list:
        '''
        Returns all connections that have not been used yet.
        '''
        return list(set(self.connections.keys()) - self.get_visited_connections())

    def count_visited_connections(self, connections_route: set):
        '''
        Counts how many times each connection has been made.
        '''
        for connection in connections_route:
            self.connections[connection] += 1

    def calculate_score(self) -> float:
        '''
        Calculates the score of the result bases on a given formula: K = p * 10000 - (T * 100 + Min).
        In which K is the quality of the generated routes, p the fraction of the used connections, T the number of routes and
        Min the total time of all routes (in minutes).
        '''
        p = len(self.get_visited_connections()) / len(self.connections)
        t = len(self.routes)
        m = 0.0
        for route in self.routes:
            m += self.routes[route].time

        score = p * 10000 - (t * 100 + m)
        return score
