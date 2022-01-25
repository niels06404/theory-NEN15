class Station():

    def __init__(self, name, x, y):
        self._name = name
        self._x = x
        self._y = y

        self._connections = {}

    def add_connection(self, direction, distance):
        '''
        Adds a connection to the station.
        '''
        self._connections[direction] = distance

    def get_possible_connections(self):
        '''
        Returns a list of all possible connections.
        '''
        return self._connections

    def __repr__(self) -> str:
        return f"{self._name}"
