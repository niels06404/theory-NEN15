from load import load_stations, load_connections
import random

def main():
    # Which funtion to run: 0 = count, 1 = create_random_route
    run = 1
    load_mode = 'Holland'
    
    stations = load_stations(f'data/Stations{load_mode}.csv')
    load_connections(f'data/Connecties{load_mode}.csv', stations)
    
    
    if run == 0:
        count_stations(stations)
    elif run == 1:
        routes = []
        passed_stations = []
        while len(set(passed_stations)) < len(stations):
            if len(routes) >= 7:
                break
            route, passed_stations = create_random_route(stations, passed_stations)
            if route != 1:
                routes.append(route)
    
        # Calculate score
        minutes = 0
        for tra in routes:
            minutes += tra[-1]
        score = 10000 * len(set(passed_stations)) / len(stations) - (len(routes) * 100 + minutes)
        
        # Print output
        for i in range(len(routes)):
            print(f"Traject {i + 1} ({int(routes[i][-1])} min): ", end='')
            print(*routes[i][:-1], sep=' | ')
            print()
                
        print("Score:", score)
        
    
def count_stations(stations):
    count = {}
    for station in stations:
        print(f"{stations[station]._name}: {len(stations[station]._connections)}")
        
        if len(stations[station]._connections) not in count:
            count[len(stations[station]._connections)] = 0
        
        count[len(stations[station]._connections)] += 1        
    print()
    print(count)


def create_random_route(stations, passed_stations):
    route = []
    time = 0
    flag = 0
    passed_stations1 = passed_stations.copy()
    
    # Get random station as starting point
    start = random.choice(list(stations))
    
    while len(route) < 1:
        if start in passed_stations:
            # 90 percent chance to skip if already in route
            if random.random() < 0.9:
                route.append(stations[start]._name)
                passed_stations.append(stations[start]._name)
            else:
                start = random.choice(list(stations))
        else:
            route.append(stations[start]._name)
            passed_stations.append(stations[start]._name)

    # Stop appending if time exceeds limit
    while time < 120:
        # Make sure the program stops if there are no more connections possible
        for x in stations[route[-1]]._connections:             
            if flag == len(route):
                if len(route) <= 5:
                        return 1, passed_stations1
        
                route.append(time)
                return route, passed_stations
            
            if x not in route:
                flag = 0
                break
            else:
                flag += 1
                
        # Add random station to route if it is not already in route    
        connection = random.choice(list(stations[route[-1]]._connections))
        
        if connection not in route:
            if connection in passed_stations:
                # 90% chance to skip if already in route
                if random.random() < 0.9:
                    break                  
            time += stations[route[-1]]._connections[connection]
            if time < 120:
                route.append(stations[connection]._name)
                passed_stations.append(stations[connection]._name)
            else:
                time -= stations[route[-1]]._connections[connection]
                break
    
    if len(route) <= 5:
            return 1, passed_stations1
    
    route.append(time)
    return route, passed_stations
  
       
if __name__ == '__main__':
    main()
