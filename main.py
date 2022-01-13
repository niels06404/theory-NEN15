from load import load_stations, load_connections
import random

def main():
    load_mode = 'Nationaal'
    
    stations = load_stations(f'data/Stations{load_mode}.csv')
    load_connections(f'data/Connecties{load_mode}.csv', stations)

    # Test
    # print(stations)
    # print(stations["Rotterdam Centraal"]._connections)
    trajects = []
    passed_stations = []
    while len(passed_stations) != len(stations):
        traject, passed_stations = create_random_traject(stations, passed_stations)
        if traject != 1:
            trajects.append(traject)
    
    # Calculate score
    minutes = 0
    for tra in trajects:
        minutes += tra[-1]
    score = 10000 * len(passed_stations) / len(stations) - (len(trajects) * 100 + minutes)
    
    # Print output
    for i in range(len(trajects)):
        print(f"Traject {i + 1} ({int(trajects[i][-1])} min): ", end='')
        print(*trajects[i][:-1], sep=' | ')
        print()
            
    print("Score:", score)
    
    # best random result so far
    ## Traject 1 (75 min): Den Haag Centraal | Leiden Centraal | Alphen a/d Rijn | Gouda | Rotterdam Alexander | Rotterdam Centraal | Schiedam Centrum | Delft
    ## Traject 2 (108 min): Schiphol Airport | Amsterdam Zuid | Amsterdam Amstel | Amsterdam Centraal | Amsterdam Sloterdijk | Haarlem | Beverwijk | Castricum | Zaandam | Hoorn
    ##Score: 9617.0
    

def create_random_traject(stations, passed_stations):
    traject = []
    time = 0
    flag = 0
    
    # Get random station as starting point
    start = random.choice(list(stations))
    while start in passed_stations:
        start = random.choice(list(stations))

    traject.append(stations[start]._name)
    passed_stations.append(stations[start]._name)
    
    # Stop appending if time exceeds limit
    while time < 120:
        # Make sure the program stops if there are no more connections possible
        for x in stations[traject[-1]]._connections:             
            if flag == len(traject):
                if len(traject) == 1:
                        return 1, passed_stations
        
                traject.append(time)
                return traject, passed_stations
            
            if x not in traject and x not in passed_stations:
                flag = 0
                break
            else:
                flag += 1
                
        # Add random station to traject if it is not already in traject    
        connection = random.choice(list(stations[traject[-1]]._connections))
        
        if connection not in traject and connection not in passed_stations:                    
            time += stations[traject[-1]]._connections[connection]
            if time < 120:
                traject.append(stations[connection]._name)
                passed_stations.append(stations[connection]._name)
            else:
                time -= stations[traject[-1]]._connections[connection]
                break
    
    if len(traject) == 1:
            return 1, passed_stations
    
    traject.append(time)
    return traject, passed_stations
  
       
if __name__ == '__main__':
    main()
