import copy
import random

class Greedy:
    def __init__(self, graph, the_map):
        self.graph = copy.deepcopy(graph)
        self.map = the_map
        self.MAX_LENGTH = 20 if the_map == "Nationaal" else 7
        self.MAX_TIME = 180 if the_map == "Nationaal" else 120
 
    def run(self):
        unavailable_options = set()
        stations_passed_list = []
        # Keep adding routes until max amount is reached or all stations are connected
        while not len(self.graph.routes) >= self.MAX_LENGTH and len(self.graph.get_visited_connections()) < len(self.graph.connections):

            starting_station = self.get_best_starting_station(stations_passed_list)

            self.graph.add_route(self.graph.stations[starting_station._name])

            key = list(self.graph.routes.keys())[-1]
            route = self.graph.routes[key]

            while route.time < self.MAX_TIME:
                # Unavailable_options prevents that a station is visited multiple times in one route
                for station in route.stations:
                    unavailable_options.add(station._name)

                possibilities = route.get_possibilities(unavailable_options)
                
                if len(possibilities) == 0:
                    unavailable_options = set()
                    break
                
                # Possibilities: station names, possibilities1: station objects
                possibilities1 = []
                for poss in possibilities:
                    possibilities1.append(self.graph.stations[poss])

                choice = self.get_best_station(possibilities1)

                route.add_station(self.graph.stations[choice._name], route.stations[-1]._connections[choice._name])

                # When time spend in the route is more than the max given time, the last connection and station is deleted
                if route.time > self.MAX_TIME:
                    route.time -= route.stations[-2]._connections[choice._name]
                    route.connections.remove((route.stations[-2]._name, route.stations[-1]._name))
                    route.stations.pop()
                    unavailable_options = set()
                    break

                unavailable_options = set()

            if not route.is_valid(self.map):
                self.graph.routes.popitem()
            elif route.is_valid(self.map):
                self.graph.count_visited_connections(route.connections)
                stations_passed_list.append(starting_station)

    # Get station with the least amount of possible connections
    def get_best_station(self, possibilities):
        possibilities.sort(key=lambda station: len(station._connections))

        return possibilities[0]

    # Get starting station with the least amount of possible connections
    def get_best_starting_station(self, stations_list):
        stations = list(self.graph.stations.values())
        
        if len(stations_list) > 0:
            for st in stations_list:
                stations.remove(st)

        stations.sort(key=lambda station: len(station._connections))

        return stations.pop(0)


class RandomGreedy(Greedy):
    def get_best_station(self, possibilities):
        possibilities.sort(key=lambda station: len(station._connections))

        return random.choice(possibilities)


class ReverseGreedy(Greedy):
    def get_best_station(self, possibilities):
        possibilities.sort(key=lambda station: len(station._connections), reverse=True)

        return possibilities[0]


class NewGreedy(Greedy):
    def get_best_station(self, possibilities):        
        # Creates list with tuples of possible connections from last route last station
        for route in list(self.graph.routes.keys())[-1:]:
            possible_connections = []
            for possibility in possibilities:
                possible_connections.append((self.graph.routes[route].stations[-1]._name, possibility._name))

        # Creates a dict with the station and the amount of connections made, vb: {"Alkmaar": 1, "Utrecht": 3}
        new_dict = {}
        for connection in possible_connections:
            new_dict[connection[1]] = self.graph.connections[connection]
            new_dict[connection[1]] += self.graph.connections[(connection[1], connection[0])]
        
        # Return station with the least amount of connections
        return self.graph.stations[(min(new_dict.items(), key=lambda x: x[1])[0])]


# NOTE: reverseNewGreedy met connecties volgen en in reverse order
# NOTE: start station kiezen op basis van minste opties, als een station al bezocht is, deze uit deze lijst halen. Mocht deze lijst leeg zijn,
# dan random een station kiezen.
# NOTE: alle stations die maar een kant op kunnen altijd weghalen als gepasseerd worden