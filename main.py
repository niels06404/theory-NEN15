import argparse
import random
import re
from code.classes.stations_graph import StationsGraph
from code.run import run_algorithm

import pandas as pd  # type: ignore


def main(the_map: str, RUNS: int, visual: int, algorithms: str, seed: int):
    # Load data into the graph
    stations_graph = StationsGraph(f"data/Stations{the_map}.csv", f"data/Connecties{the_map}.csv")

    # ---------------------------------------------------- Input handling ----------------------------------------------------
    # Setup algorithms available to run
    choices = ["AdaptedGreedy", "Greedy", "NewRandom", "RandomGreedy", "Random"]

    raw_algorithms = algorithms.split(",")
    algorithm_list = []
    duplicates = set()

    # Check correctness of input
    for raw_algorithm in raw_algorithms:
        if re.match("(?:^)[1-5][h](?:$)", raw_algorithm.strip().lower()) and raw_algorithm.strip()[0] not in duplicates:
            algorithm_list.append((choices[int(raw_algorithm.strip()[0]) - 1], True))
            duplicates.add(raw_algorithm.strip()[0])
        elif re.match("(?:^)[1-5](?:$)", raw_algorithm.strip()) and raw_algorithm.strip()[0] not in duplicates:
            algorithm_list.append((choices[int(raw_algorithm.strip()) - 1], False))
            duplicates.add(raw_algorithm.strip()[0])
        else:
            raise Exception("Error, argument -a invalid, example input: 1,2h,3,4,5h")

    if seed is None:
        seed = int(random.random() * 100000000)

    # ---------------------------------------------------------- Run ---------------------------------------------------------
    results = {}
    for algorithm in algorithm_list:
        result = run_algorithm(algorithm[0], stations_graph, the_map, RUNS, hill=algorithm[1], seed=seed)
        results["best" + algorithm[0]], results["scores" + algorithm[0]], results["all" + algorithms[0]] = result

        if visual:
            from code.visualization.visualization import visualization

            print(f"Loading visualization of best {algorithm[0]} result...")
            visualization(the_map, results["best" + algorithm[0]], algorithm[0])
            print(f"Done! See '{the_map}_{algorithm[0]}_routes.png' for visualization of {algorithm[0]}.")

    # -------------------------------------------------------- Output --------------------------------------------------------
    # Save random graph to .csv file
    output = random.choice(algorithm_list)[0]
    generate_output(results["best" + output], "output.csv")
    print(f"See 'output.csv' for generated routes of algorithm {output}.")


def generate_output(graph: StationsGraph, output_file: str):
    '''
    Creates a .csv file with the generated output in line with the expected format.
    '''
    # Create empty dataframe with columns to store the info from the tracks
    tracks_df = pd.DataFrame(columns=["train", "stations"])

    for i, route in enumerate(graph.routes.values()):
        tracks_df = tracks_df.append(pd.DataFrame([["train_" + str(i + 1), "[" + ","
                                                    .join([str(route.stations[j]._name)
                                                           for j in range(len(route.stations))]) + "]"]],
                                                  columns=["train", "stations"]))

    tracks_df = tracks_df.append(pd.DataFrame([["score", graph.calculate_score()]], columns=["train", "stations"]))

    # Save results to output .csv file
    tracks_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Create train trajects")

    # Adding arguments
    parser.add_argument("the_map", choices=["Nationaal", "Holland"])
    parser.add_argument("-N", help="Number of runs (default: 1)", type=int, default=1)
    parser.add_argument("-V", help="Execute visualisation (default: True)", type=int, default=0, choices=[0, 1])
    parser.add_argument("-a", help="Algorithms to run [1=AdaptedGreedy, 2=Greedy, 3=NewRandom, 4=RandomGreedy, 5=Random]. " +
                        "Add 'h' after number to also run hillclimber.", default="5,1", type=str)
    parser.add_argument("-s", help="Random seed", type=int, default=None)

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.the_map, args.N, args.V, args.a, args.s)
