from load import load_stations, load_connections


stations = load_stations("inputFiles/StationsHolland.csv")
load_connections("inputFiles/ConnectiesHolland.csv", stations)

# Test
print(stations)
print(stations["Rotterdam Centraal"]._connections)

