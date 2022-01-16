import argparse
from code.algorithms import randomize
from code.classes.stations_graph import StationsGraph

import pandas as pd


def main(the_map, output_file):
    # Load data into the graph
    stations_graph = StationsGraph(f'data/Stations{the_map}.csv', f'data/Connecties{the_map}.csv')

    # Random solution
    best_graph = None
    best_score = 0
    for _ in range(1):
        random_graph = randomize.random_assignment(stations_graph)
        if random_graph.calculate_score() > best_score:
            best_graph = random_graph
            best_score = random_graph.calculate_score()
    print(f"Random algorithm completed successfully with a score of {best_graph.calculate_score()}.")

    # Save graph to .csv file
    generate_output(best_graph, output_file)
    print(f"See '{output_file}' for generated routes.")


def generate_output(graph, output_file):
    # Create empty dataframe with columns to store the info from the tracks.
    tracks_df = pd.DataFrame(columns=["train", "stations"])

    for i, route in enumerate(graph.routes.values()):
        tracks_df = tracks_df.append(pd.DataFrame([["train_" + str(i + 1), '[' + ', '.join([str(route.stations[j]._name) for j in range(len(route.stations))]) + ']']], columns=["train", "stations"]))

    tracks_df = tracks_df.append(pd.DataFrame([["score", graph.calculate_score()]], columns=["train", "stations"]))

    # Save results to output .csv file
    tracks_df.to_csv(output_file, index=False)


# TODO: BROKEN!!! Fix this according to new data structure
def traject_visualization(route, stations):
    from visualization import visualization
    for i in range(len(route[:-1])):
        stations[route[i]].set_connection_visited(route[i+1])


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Create train trajects")

    # Adding arguments
    parser.add_argument("the_map", choices=["Nationaal", "Holland"])
    parser.add_argument("output_file", help="output file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.the_map, args.output_file)
