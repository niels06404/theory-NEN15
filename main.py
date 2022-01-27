import argparse
import random
import sys
from code.algorithms import greedy as gr
from code.algorithms import hillclimber as hc
from code.algorithms import randomize
from code.classes.stations_graph import StationsGraph

import pandas as pd


def main(the_map, output_file, RUNS, visual):
    # Load data into the graph
    stations_graph = StationsGraph(f'data/Stations{the_map}.csv', f'data/Connecties{the_map}.csv')

    # -------------------------------------------------------- Random --------------------------------------------------------
    random.seed()

    # print("Random algorithm is running...")
    # random_graph = randomize.random_assignment(stations_graph, the_map)

    # print(f"Random algorithm completed successfully with a score of {random_graph.calculate_score()}.")
    # print()

    print(f"random algorithm is running {RUNS} times...")
    best_score = 0
    total_score = 0

    for _ in range(RUNS):
        random_graph = randomize.random_assignment(stations_graph, the_map)

        if random_graph.calculate_score() > best_score:
            best_random_graph = random_graph
            best_score = random_graph.calculate_score()
        total_score += random_graph.calculate_score()
        average_score = total_score / RUNS

    print(f"random algorithm completed successfully with a best score of {best_random_graph.calculate_score()} out of {RUNS} runs.")
    print()

    # -------------------------------------------------------- Greedy --------------------------------------------------------
    greedy = gr.Greedy(stations_graph, the_map)
    print("Greedy algorithm is running...")
    greedy.run()

    print(f"Greedy completed successfully with a score of {greedy.graph.calculate_score()}.")
    print()

    # ----------------------------------------------------- RandomGreedy -----------------------------------------------------
    random_greedy = gr.RandomGreedy(stations_graph, the_map)
    print("randomGreedy algorithm is running...")
    random_greedy.run()

    print(f"randomGreedy completed successfully with a score of {random_greedy.graph.calculate_score()}.")
    print()

    # ----------------------------------------------------- ReverseGreedy ----------------------------------------------------
    reverse_greedy = gr.ReverseGreedy(stations_graph, the_map)
    print("reverseGreedy algorithm is running...")
    reverse_greedy.run()

    print(f"reverseGreedy completed successfully with a score of {reverse_greedy.graph.calculate_score()}.")
    print()

    # ----------------------------------------------------- AdaptedGreedy ----------------------------------------------------
    random.seed()

    adapted_greedy = gr.AdaptedGreedy(stations_graph, the_map)
    print("adaptedGreedy algorithm is running...")
    adapted_greedy.run()

    print(f"adaptedGreedy algorithm completed successfully with a score of {adapted_greedy.graph.calculate_score()}.")
    print()

    # print(f"adaptedGreedy algorithm is running {RUNS} times...")
    # best_score = 0
    # total_score = 0

    # for _ in range(RUNS):
    #     adapted_greedy = gr.AdaptedGreedy(stations_graph, the_map)
    #     adapted_greedy.run()

    #     if adapted_greedy.graph.calculate_score() > best_score:
    #         best_adapted_greedy = adapted_greedy
    #         best_score = adapted_greedy.graph.calculate_score()
    #     total_score += adapted_greedy.graph.calculate_score()
    #     average_score = total_score / RUNS

    # print(f"adaptedGreedy completed successfully with a best score of {best_adapted_greedy.graph.calculate_score()} out of {RUNS} runs.")
    # print()

    # ------------------------------------------------------ HillClimber -----------------------------------------------------
    random.seed()

    hillclimber = hc.HillClimber(adapted_greedy.graph, the_map)
    print("HillClimber algorithm is running ...")
    hillclimber.run()

    print(f"HillClimber completed successfully with a score of {hillclimber.graph.calculate_score()}.")
    print()

    # TODO: Nationaal plot genereren met adaptedGreedy en HillClimber

    # -------------------------------------------------------- Output --------------------------------------------------------
    # Save graph to .csv file
    generate_output(hillclimber.graph, output_file)
    print(f"See '{output_file}' for generated routes.")

    # Output info to file for personal use
    generate_personal_output(best_random_graph, average_score, RUNS)

    # Visualize results on map
    if visual:
        from visualization import visualization

        print("Loading visualization...")
        visualization(the_map, hillclimber.graph)
        print(f"Done! See '{the_map}_routes.png' for visualization.")


def generate_personal_output(graph, average_score, RUNS):
    from visualization import cleanup_connections

    sys.stdout = open("output.txt", "w")
    for i, route in enumerate(graph.routes.values()):
        print(f"Route {i + 1}", end=': ')
        for station in route.stations:
            print(station._name, end=', ')
        print("Time:", route.time)
    print()
    print("Unvisited connections:", cleanup_connections(graph.get_unused_connections()), ", Length:", len(cleanup_connections(graph.get_unused_connections())))
    print("p =", len(graph.get_visited_connections()) / len(graph.connections))
    print("T =", len(graph.routes))
    print("Min =", sum([route.time for route in graph.routes.values()]))
    print("Score:", graph.calculate_score())
    print(f"Average score: {average_score} out of {RUNS} runs")
    sys.stdout.close()
    sys.stdout = sys.__stdout__


def generate_output(graph, output_file):
    # Create empty dataframe with columns to store the info from the tracks
    tracks_df = pd.DataFrame(columns=["train", "stations"])

    for i, route in enumerate(graph.routes.values()):
        tracks_df = tracks_df.append(pd.DataFrame([["train_" + str(i + 1), '[' + ', '.join([str(route.stations[j]._name) for j in range(len(route.stations))]) + ']']], columns=["train", "stations"]))

    tracks_df = tracks_df.append(pd.DataFrame([["score", graph.calculate_score()]], columns=["train", "stations"]))

    # Save results to output .csv file
    tracks_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Create train trajects")

    # Adding arguments
    parser.add_argument("the_map", choices=["Nationaal", "Holland"])
    parser.add_argument("output_file", help="output file (csv)")
    parser.add_argument("-N", help="Number of runs (default: 1)", type=int, default=1)
    parser.add_argument("-V", help="Execute visualisation (default: True)", type=int, default=1, choices=[0, 1])

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.the_map, args.output_file, args.N, args.V)
