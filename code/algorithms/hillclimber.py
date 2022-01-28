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
        self.MAX_LENGTH = 20 if the_map == "Nationaal" else 7
        self.MAX_TIME = 180 if the_map == "Nationaal" else 120

    def run(self):
        '''
        Executes the algorithm.
        '''
        # Try to get a better solution by removing end stations from routes
        self.update_last_station_del()

        # Try to get a better solution by removing routes with an increasing length
        self.update_short_routes()

        # Try to get a better solution by merging two routes together
        self.update_merge_station()

        # Get unused connections and check if list is not empty
        unused_connections = [connection for connection in self.graph.connections if (self.graph.connections[connection] == 0 and self.graph.connections[(connection[1], connection[0])] == 0)]
        if unused_connections:
            # Try to get a better solution by adding unused connections at the end of a route
            self.update_last_station_add(unused_connections)

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

    def update_last_station_del(self):
        '''
        Removes last station from a route if it gives a better score.
        '''
        route_list = self.get_all_routes()
        while route_list:
            route = random.choice(route_list)

            self.graph.routes[route].remove_last_station()

            if self.best_score < self.graph.calculate_score() and len(self.graph.routes[route].stations) != 1:
                self.best_score = self.graph.calculate_score()
                self.backup_graph = pickle.loads(pickle.dumps(self.graph))
            else:
                route_list.remove(route)
                self.graph = pickle.loads(pickle.dumps(self.backup_graph))
    
    def update_merge_station(self):
        '''
        Merges two different routes
        '''
        route_list = self.get_all_routes()
        while route_list:
            route = random.choice(route_list)

            time_route = self.graph.routes[route].time
            route_list2 = self.get_all_routes()
            for other_route in route_list2:
                time_other_route = self.graph.routes[other_route].time
                if other_route == route or time_route + time_other_route > self.MAX_TIME:
                    continue
                
                connection = (self.graph.routes[route].stations[-1]._name, self.graph.routes[other_route].stations[1]._name)
                if connection in self.graph.connections:
                    self.graph.routes[route].stations.extend(self.graph.routes[other_route].stations[1:])
                    self.graph.routes[route].connections.add(connection)
                    self.graph.routes[route].time += time_other_route
                    
                    del self.graph.routes[other_route]

                    if self.best_score < self.graph.calculate_score():
                        self.best_score = self.graph.calculate_score()
                        self.backup_graph = pickle.loads(pickle.dumps(self.graph))
                        if other_route in route_list:
                            route_list.remove(other_route)
                    else:
                        self.graph = pickle.loads(pickle.dumps(self.backup_graph))       

            route_list.remove(route)
    
    def update_last_station_add(self, unused_connections):
        '''
        Adds unused connection to the end of a
        '''
        route_list = self.get_all_routes()
        end_stations = {}
        best_time = self.MAX_TIME
        for route in route_list:
            if self.graph.routes[route].stations[-1]._name in end_stations:
                if self.graph.routes[route].time < best_time:
                    best_time = self.graph.routes[route].time
                    end_stations[self.graph.routes[route].stations[-1]._name] = self.graph.routes[route]
            else:
                best_time = self.graph.routes[route].time
                end_stations[self.graph.routes[route].stations[-1]._name] = self.graph.routes[route]

        while unused_connections and end_stations:
            for connection in unused_connections:
                for station in connection:
                    if station in end_stations:
                        if self.graph.stations[[st for st in connection if st != station][0]] not in end_stations[station].stations:
                            end_stations[station].add_station(self.graph.stations[[st for st in connection if st != station][0]], self.graph.stations[station]._connections[[st for st in connection if st != station][0]])
                            if end_stations[station].time > self.MAX_TIME or self.graph.calculate_score() < self.best_score:
                                end_stations[station].remove_last_station()
                                self.graph = pickle.loads(pickle.dumps(self.backup_graph))
                            else:
                                self.best_score = self.graph.calculate_score()
                                self.backup_graph = pickle.loads(pickle.dumps(self.graph)) 
                                end_stations[[st for st in connection if st != station][0]] = end_stations[station]   
                        del end_stations[station]
                unused_connections.remove(connection)

    def get_all_routes(self):
        '''
        Saves all the keys of the routes in a list
        '''
        route_list = []
        for route in self.graph.routes:
            route_list.append(route)
        return route_list
