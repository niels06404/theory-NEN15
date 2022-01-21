import copy
import random


def random_assignment(input_graph, the_map):
    '''
    Randomly assigns valid stations to routes.
    '''
    graph = copy.deepcopy(input_graph)

    unavailable_options = set()
    if the_map == "Nationaal":
        MAX_LENGTH = 20
        MAX_TIME = 180
    else:
        MAX_LENGTH = 7
        MAX_TIME = 120

    # Keep adding routes until max amount is reached or all stations are connected
    while not len(graph.routes) >= MAX_LENGTH and len(graph.get_visited_connections()) < len(graph.connections):
        # First element can pick any station
        starting_station = random.choice(list(graph.stations))

        # Create a new route with starting station
        graph.add_route(graph.stations[starting_station])

        # Keep adding stations to route until time exceeds limit
        key = list(graph.routes.keys())[-1]
        route = graph.routes[key]
        while route.time < MAX_TIME:
            # Stop algorithm from visiting the same station twice in one route
            # NOTE: Can be changed to not allowing duplicate connections at all or only allowing revisiting after n steps, for example.
            for station in route.stations:
                unavailable_options.add(station._name)

            possibilities = route.get_possibilities(unavailable_options)

            # Stop adding if no options are left
            if len(possibilities) == 0:
                unavailable_options = set()
                break
            # Otherwise randomly pick a station
            choice = random.choice(possibilities)

            # Add randomly picked station to route
            route.add_station(graph.stations[choice], route.stations[-1]._connections[choice])
            unavailable_options = set()

        # Remove route if it is not valid
        if not route.is_valid(the_map):
            graph.routes.popitem()
        elif route.is_valid(the_map):
            graph.count_visited_connections(route.connections)

    return graph
