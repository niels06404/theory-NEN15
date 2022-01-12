from load import load_stations, load_connections

def main():
    load_mode = 'Holland'
    
    stations = load_stations(f'data/Stations{load_mode}.csv')
    load_connections(f'data/Connecties{load_mode}.csv', stations)

    # Test
    print(stations)
    print(stations["Rotterdam Centraal"]._connections)


if __name__ == '__main__':
    main()
