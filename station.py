class Station():
    
    def __init__(self, name, x, y):
        self._name = name
        self._x = x
        self._y = y
        self._connections = {}
        self._connections_loc = {}

    # vb connections: {station1: 30, station2: 40, ...}
    def add_connection(self, direction, distance):
        self._connections[direction] = distance
    
    def add_connection_loc(self, direction, x, y):
        self._connections_loc[direction] = x, y


