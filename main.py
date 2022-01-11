from load import load_stations, load_connections


stations = load_stations("data/StationsHolland.csv")
load_connections("data/ConnectiesHolland.csv", stations)

# Test
print(stations)
print(stations["Rotterdam Centraal"]._connections)

