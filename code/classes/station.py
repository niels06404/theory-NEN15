class Station():

    def __init__(self, name: str, x: float, y: float):
        self._name = name
        self._x = x
        self._y = y

        self._connections: dict[str, float] = {}

    def add_connection(self, direction: str, distance: float):
        '''
        Adds a connection to the station.
        '''
        self._connections[direction] = distance

    def get_possible_connections(self) -> dict:
        '''
        Returns a dictionary of all possible connections.
        '''
        return self._connections

    def __repr__(self) -> str:
        return f"{self._name}"
