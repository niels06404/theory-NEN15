# import copy
import pickle
import random


class HillClimber:
    def __init__(self, input_graph, the_map):
        if not input_graph.is_solution(the_map):
            raise Exception("HillClimber requires a complete solution.")

        # self.graph = copy.deepcopy(input_graph)
        self.graph = pickle.loads(pickle.dumps(input_graph))
        self.best_score = self.graph.calculate_score()
        # self.backup_graph = copy.deepcopy(self.graph)
        self.backup_graph = pickle.loads(pickle.dumps(self.graph))

    def run(self):
        '''
        Executes the algorithm.
        '''
        # Try to get a better solution by removing end stations from routes
        self.update_last_station()

        # Try to get a better solution by removing routes with an increasing length
        self.update_short_routes()

        # TODO: kijken of connecties met 0 toegevoegd kunnen worden aan trajecten

    def update_short_routes(self):
        '''
        Removes routes if it gives a better score.
        '''
        for i in range(2, 20):
            route_list = self.get_all_routes()

            while route_list:
                route = random.choice(route_list)

                if len(self.graph.routes[route].stations) == i:
                    del self.graph.routes[route]

                    if self.best_score < self.graph.calculate_score():
                        self.best_score = self.graph.calculate_score()
                        # self.backup_graph = copy.deepcopy(self.graph)
                        self.backup_graph = pickle.loads(pickle.dumps(self.graph))
                    else:
                        # self.graph = copy.deepcopy(self.backup_graph)
                        self.graph = pickle.loads(pickle.dumps(self.backup_graph))

                route_list.remove(route)

    def update_last_station(self):
        '''
        Removes last station from a route if it gives a better score.
        '''
        route_list = self.get_all_routes()
        while route_list:
            route = random.choice(route_list)

            self.graph.routes[route].remove_last_station()

            if self.best_score < self.graph.calculate_score() and len(self.graph.routes[route].stations) != 1:
                self.best_score = self.graph.calculate_score()
                # self.backup_graph = copy.deepcopy(self.graph)
                self.backup_graph = pickle.loads(pickle.dumps(self.graph))
            else:
                route_list.remove(route)
                # self.graph = copy.deepcopy(self.backup_graph)
                self.graph = pickle.loads(pickle.dumps(self.backup_graph))

    def get_all_routes(self):
        '''
        Saves all the keys of the routes in a list
        '''
        route_list = []
        for route in self.graph.routes:
            route_list.append(route)
        return route_list
