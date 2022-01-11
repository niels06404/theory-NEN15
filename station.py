class Station():
    
    def __init__(self, name, x, y):
        self._name = name
        self._x = x
        self._y = y
        self._connections = {}

    # vb connections: {station1: 30, station2: 40, ...}
    def add_connection(self, direction, distance):
        self._connections[direction] = distance


