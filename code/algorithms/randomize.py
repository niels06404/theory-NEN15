import copy
import random
from code.classes.station import Station
from code.classes.stations_graph import StationsGraph


class Random:
    def __init__(self, input_graph: StationsGraph, the_map: str):
        self.graph = copy.deepcopy(input_graph)
        self.map = the_map
        self.MAX_LENGTH = 20 if the_map == "Nationaal" else 7
        self.MAX_TIME = 180 if the_map == "Nationaal" else 120

    def run(self):
        '''
        Executes the algorithm.
        '''
        unavailable_options = set()
        length_connections = len(self.graph.connections)
        while len(self.graph.routes) < self.MAX_LENGTH and len(self.graph.get_visited_connections()) < length_connections:
            starting_station = self.get_starting_station()

            # Create a new route with starting station
            self.graph.add_route(self.graph.stations[starting_station])

            # Keep adding stations to route until time exceeds limit
            key = list(self.graph.routes.keys())[-1]
            route = self.graph.routes[key]

            while route.time < self.MAX_TIME:
                # Stop algorithm from visiting the same station twice in one route
                for station in route.stations:
                    unavailable_options.add(station._name)

                possibilities = route.get_possibilities(unavailable_options)

                # Stop adding if no options are left
                if len(possibilities) == 0:
                    unavailable_options = set()
                    break

                # Otherwise randomly pick a station
                choice = random.choice(possibilities)

                # Add randomly picked station to route
                route.add_station(self.graph.stations[choice], route.stations[-1]._connections[choice])
                unavailable_options = set()

            # Remove route if it is not valid
            if not route.is_valid(self.map):
                del self.graph.routes[key]
            elif route.is_valid(self.map):
                self.graph.count_visited_connections(route.connections)

    def get_starting_station(self) -> Station:
        '''
        Returns a random starting station
        '''
        return random.choice(list(self.graph.stations))


class NewRandom(Random):
    def get_starting_station(self) -> Station:
        '''
        Returns a station from a connection with the least number of connections made.
        '''
        possibilities = [connection for connection in self.graph.connections if self.graph.connections[connection] == 0]
        possibility = random.choice(possibilities)
        while self.graph.connections[(possibility[1], possibility[0])] != 0:
            possibility = random.choice(possibilities)

        return random.choice(possibility)
