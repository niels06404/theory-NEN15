from load import load_stations, load_connections
from visualization import visualization
import random
import argparse
import pandas as pd


def main(the_map, output_file):
    # Which funtion to run: 0 = count, 1 = create_random_route
    run = 1
    
    stations = load_stations(f'data/Stations{the_map}.csv')
    load_connections(f'data/Connecties{the_map}.csv', stations)

    # Create empty dataframe with columns to store the info from the tracks.
    tracks_df = pd.DataFrame(columns = ["train", "stations"])
    
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
        fraction = 0
        for tra in routes:
            minutes += tra[-1]
            
        # for x in routes:
        #     for i in len(x[:-1]):
                
        
    
        score = 10000 * (len(set(passed_stations)) / 56) - (len(routes) * 100 + minutes)
        
        print("p: ", fraction / 56)
        print("T: ", len(routes))
        print("min: ", minutes)
        
        # Print output
        for i in range(len(routes)):
            print(f"Traject {i + 1} ({int(routes[i][-1])} min): ", end='')
            print(*routes[i][:-1], sep=' | ')
            print()
            # Het duurde even om uit te vinden hoe je routes opslaat, je slaat het op als : ["Den Haag", "Delft" , ..., 43.0]
            # Het lijkt me handiger om de steden binnen deze lijst in een lijst te zetten, dus: [["Den Haag", "Delft", ...], 43.0]
            # Zo kan je dit makkelijk uitschrijven als output, dit lukt me op dit moment niet, omdat het in deze vorm opgeslagen staat.
            # Deze lijst kan dan op de plek waar nu "Test" staat worden gezet.
            tracks_df = tracks_df.append(pd.DataFrame([["train_" + str(i + 1), str(routes[i][:-1]).replace("\'", "")]], columns = ["train", "stations"]))
        
        print("Score:", score)
        tracks_df = tracks_df.append(pd.DataFrame([["score", score]], columns = ["train", "stations"]))

        # Save results to output csv file
        tracks_df.to_csv(output_file, index = False)
        visualization(the_map, stations)
        
    
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
  
       
if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "Create train trajects")

    # Adding arguments
    parser.add_argument("the_map", choices=["Nationaal", "Holland"])
    parser.add_argument("output_file", help = "output file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.the_map, args.output_file)
