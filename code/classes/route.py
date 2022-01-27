class Route():
    def __init__(self, starting_station):
        self.stations = [starting_station]
        self.time = 0
        self.connections = set()

    def is_valid(self, the_map):
        '''
        Returns True if the route is valid according to the given restrictions.
        False otherwise.
        '''

        if the_map == "Nationaal":
            MAX_TIME = 180
        else:
            MAX_TIME = 120

        # Route should have at least made one connection
        if len(self.stations) < 2:
            return False

        # Route should only have connections between neighboring stations
        for i in range(len(self.stations[:-1])):
            if not self.stations[i+1]._name in self.stations[i].get_possible_connections():
                return False

        # Total time should not be greater than limit
        if self.time > MAX_TIME:
            return False

        return True

    def add_station(self, station, time):
        '''
        Adds a new station to the route.
        '''
        self.connections.add((self.stations[-1]._name, station._name))
        self.stations.append(station)
        self.time += time

    def remove_last_station(self):
        '''
        Removes the last station from the route
        '''
        self.connections.remove((self.stations[-2]._name, self.stations[-1]._name))
        self.time -= self.stations[-2]._connections[self.stations[-1]._name]
        self.stations.pop()

    def get_possibilities(self, unavailable_connections):
        '''
        Returns a list of possibilities to where a connection can be made.
        '''
        available_connections = set(self.stations[-1].get_possible_connections())

        return sorted(list(available_connections - unavailable_connections))
