import random


def random_assignment(graph):
    '''
    Randomly assigns valid stations to routes.
    '''
    unavailable_options = set()
    # Keep adding routes until max amount is reached or all stations are connected
    while not len(graph.routes) >= 7:
        # First element can pick any station
        starting_station = random.choice(list(graph.stations))

        # Create a new route with starting station
        graph.add_route(graph.stations[starting_station])

        # Keep adding stations to route until time exceeds limit
        route = graph.routes[starting_station]
        while route.time < 120:
            # Stop algorithm from visiting the same station twice in one route
            # NOTE: Can be changed to not allowing duplicate connections at all or only allowing revisiting after n steps, for example.
            for station in route.stations:
                unavailable_options.add(station._name)

            possibilities = route.get_possibilities(unavailable_options)

            # Stop adding if no options are left
            if len(possibilities) == 0:
                break
            # Otherwise randomly pick a station
            choice = random.choice(possibilities)

            # Add randomly picked station to route
            route.add_station(graph.stations[choice], route.stations[-1]._connections[choice])
            unavailable_options = set()

        # Remove route if it is not valid
        if not route.is_valid():
            graph.routes.pop(starting_station)

    return graph
