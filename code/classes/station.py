class Station():

    def __init__(self, name, x, y):
        self._name = name
        self._x = x
        self._y = y
        self._passed = False
        self._connections = {}
        self._connections_loc = {}

    def add_connection(self, direction, distance):
        '''
        Adds a connection to the station.
        '''
        self._connections[direction] = distance

    def add_connection_loc(self, direction, x, y):
        '''
        Adds the coordinates of the end point of the connection the the station and defaults visited to False.
        '''
        self._connections_loc[direction] = [(x, y), False]

    def set_connection_visited(self, direction):
        '''
        Marks the connection as visited if there is a connection present.
        '''
        self._connections_loc[direction][1] = True

    def get_possible_connections(self):
        '''
        Returns a list of all possible connections.
        '''
        return self._connections
