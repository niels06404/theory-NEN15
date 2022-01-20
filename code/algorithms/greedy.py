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
                for station in route.stations:
                    unavailable_options.add(station._name)
                # if len(route.stations) > 1:
                #     unavailable_options.add(route.stations[-2]._name)

                possibilities = route.get_possibilities(unavailable_options)
                
                if len(possibilities) == 0:
                    unavailable_options = set()
                    break

                possibilities1 = []
                for poss in possibilities:
                    possibilities1.append(self.graph.stations[poss])

                choice = self.get_best_station(possibilities1)

                route.add_station(self.graph.stations[choice._name], route.stations[-1]._connections[choice._name])
                if route.time > self.MAX_TIME:
                    route.time -= route.stations[-2]._connections[choice._name]
                    route.stations.pop()
                    unavailable_options = set()
                    break

                unavailable_options = set()

            # NOTE: pas toevoegen als route valid is (alle stations van route)
            if not route.is_valid(self.map):
                self.graph.routes.popitem()
            elif route.is_valid(self.map):
                self.graph.count_visited_connections(route.connections)
                stations_passed_list.append(starting_station)

    def get_best_station(self, possibilities):
        possibilities.sort(key=lambda station: len(station._connections))

        return possibilities[0]

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
