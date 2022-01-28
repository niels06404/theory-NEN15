import copy
import pickle

class NewRandom:
    def __init__(self, input_graph, the_map):
        # self.graph = copy.deepcopy(input_graph)
        self.graph = pickle.loads(pickle.dumps(input_graph))
        self.map = the_map
        self.MAX_LENGTH = 20 if the_map == "Nationaal" else 7
        self.MAX_TIME = 180 if the_map == "Nationaal" else 120
    
    def run(self):
        unavailable_options = set()
        # while not len(self.graph.routes) >= self.MAX_LENGTH and len(self.graph.get_visited_connections()) < len(self.graph.connections):
        #     pass
        for connection in self.graph.connections:
            print(connection, self.graph.connections[connection])
    
    def get_starting_station(self):
        possibilities = [connection for connection in self.graph.connections if self.graph.connections[connection] == 0]
        

        # # Get last station from route and create tuples of all possible connections
        # for route in list(self.graph.routes.keys())[-1:]:
        #     possible_connections = []
        #     for possibility in possibilities:
        #         possible_connections.append((self.graph.routes[route].stations[-1]._name, possibility._name))

        # # Count number of made connections for both directions
        # new_dict = {}
        # for connection in possible_connections:
        #     new_dict[connection[1]] = self.graph.connections[connection]
        #     new_dict[connection[1]] += self.graph.connections[(connection[1], connection[0])]

        # # Return station with the least amount of connections
        # result = self.get_random_minimum(new_dict, lambda x: x[1])

        # return self.graph.stations[result]
