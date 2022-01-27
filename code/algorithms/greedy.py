# import copy
import pickle
import random


class Greedy:
    def __init__(self, input_graph, the_map):
        # self.graph = copy.deepcopy(input_graph)
        self.graph = pickle.loads(pickle.dumps(input_graph))
        self.map = the_map
        self.MAX_LENGTH = 20 if the_map == "Nationaal" else 7
        self.MAX_TIME = 180 if the_map == "Nationaal" else 120

    def run(self):
        '''
        Executes the algorithm.
        '''
        unavailable_options = set()
        stations_passed_list = []
        # Keep adding routes until max amount is reached or all stations are connected
        while not len(self.graph.routes) >= self.MAX_LENGTH and len(self.graph.get_visited_connections()) < len(self.graph.connections):
            starting_station = self.get_best_starting_station(stations_passed_list)

            self.graph.add_route(self.graph.stations[starting_station._name])

            # Select current route
            key = list(self.graph.routes.keys())[-1]
            route = self.graph.routes[key]

            while route.time < self.MAX_TIME:
                # Make sure a station is not visited multiple times in one route
                for station in route.stations:
                    unavailable_options.add(station._name)

                # Stations with one possible direction can only be at the beginning of a route
                for station in self.graph.stations:
                    if len(self.graph.stations[station]._connections) == 1:
                        unavailable_options.add(self.graph.stations[station]._name)

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

                # When time spent in the route is more than the max given time, the last connection and station is deleted
                if route.time > self.MAX_TIME:
                    route.time -= route.stations[-2]._connections[choice._name]
                    route.connections.remove((route.stations[-2]._name, route.stations[-1]._name))
                    route.stations.pop()
                    unavailable_options = set()
                    break

                unavailable_options = set()

            # Check if the generated route is valid, if it is not remove the whole route
            if not route.is_valid(self.map):
                self.graph.routes.popitem()
            elif route.is_valid(self.map):
                self.graph.count_visited_connections(route.connections)
                stations_passed_list = self.add_stations(stations_passed_list)

    def add_stations(self, stations_passed_list):
        '''
        Adds all stations in the route to a list of passed stations.
        '''
        for station in self.graph.routes[list(self.graph.routes.keys())[-1]].stations:
            if station not in stations_passed_list:
                stations_passed_list.append(station)

        return stations_passed_list

    def get_best_station(self, possibilities):
        '''
        Returns the station with the least possible connections.
        '''
        possibilities.sort(key=lambda station: len(station._connections))

        return possibilities[0]

    def get_best_starting_station(self, stations_list):
        '''
        Returns the starting station with the least possible connections. If all stations are visited at least once,
        return a random station which has one or more open connections.
        '''
        stations = list(self.graph.stations.values())

        # Remove visited stations from possibilities
        if len(stations_list) > 0:
            for station in stations_list:
                stations.remove(station)

        if len(stations) > 0:
            stations.sort(key=lambda station: len(station._connections))
        else:
            # Return a random station with the fewest made connections
            new_dict = {}
            for connection in self.graph.connections:
                new_dict[connection] = self.graph.connections[connection] + self.graph.connections[(connection[1], connection[0])]

            result = self.get_random_minimum(new_dict, lambda x: x[1])[0]
            return self.graph.stations[result]

        return stations[0]

    def get_random_minimum(self, dict_items, func):
        '''
        Returns a random key from a dictionary with a value equal to the minimum value in the dictionary.
        '''
        minimum = min(dict_items.items(), key=func)[1]
        keys = [k for k, v in dict_items.items() if v == minimum]
        keys.sort()

        return random.choice(keys)


class RandomGreedy(Greedy):
    def get_best_station(self, possibilities):
        '''
        Returns a random station from the possibilities.
        '''
        return random.choice(possibilities)


class ReverseGreedy(Greedy):
    def get_best_station(self, possibilities):
        '''
        Returns the station with the most possible connections.
        '''
        possibilities.sort(key=lambda station: len(station._connections), reverse=True)

        return possibilities[0]


class AdaptedGreedy(Greedy):
    def get_best_station(self, possibilities):
        '''
        Returns the station with the least number of possibilities while also preffering stations with the least number of
        connections made.
        '''
        # Get last station from route and create tuples of all possible connections
        for route in list(self.graph.routes.keys())[-1:]:
            possible_connections = []
            for possibility in possibilities:
                possible_connections.append((self.graph.routes[route].stations[-1]._name, possibility._name))

        # Count number of made connections for both directions
        new_dict = {}
        for connection in possible_connections:
            new_dict[connection[1]] = self.graph.connections[connection]
            new_dict[connection[1]] += self.graph.connections[(connection[1], connection[0])]

        # Return station with the least amount of connections
        result = self.get_random_minimum(new_dict, lambda x: x[1])

        return self.graph.stations[result]
