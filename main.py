import argparse
import sys
from code.algorithms import greedy as gr
from code.algorithms import randomize
from code.classes.stations_graph import StationsGraph

import pandas as pd


# vb: python3 main.py Holland output.csv -N 10
def main(the_map, output_file, RUNS, vis):
    if RUNS == 1:
        print(f"Calculating best routes out of {RUNS} run...")
    else:
        print(f"Calculating best routes out of {RUNS} runs...")
        
    # Load data into the graph
    stations_graph = StationsGraph(f'data/Stations{the_map}.csv', f'data/Connecties{the_map}.csv')
    
    # -------------------------------------------------------- Greedy --------------------------------------------------------
    greedy_graph = gr.Greedy(stations_graph, the_map)
    print("Greedy algorithm is running...")
    greedy_graph.run()

    print(f"Greedy algorithm completed successfully with a score of {greedy_graph.graph.calculate_score()}.")
    print()    

    # ----------------------------------------------------- RandomGreedy -----------------------------------------------------
    randomGreedy_graph = gr.RandomGreedy(stations_graph, the_map)
    print("randomGreedy algorithm is running...")
    randomGreedy_graph.run()

    print(f"randomGreedy algorithm completed successfully with a score of {randomGreedy_graph.graph.calculate_score()}.")
    print()
    
    # ---------------------------------------------------- ReverseGreedy -----------------------------------------------------
    reverseGreedy_graph = gr.ReverseGreedy(stations_graph, the_map)
    print("reverseGreedy algorithm is running...")
    reverseGreedy_graph.run()

    print(f"reverseGreedy algorithm completed successfully with a score of {reverseGreedy_graph.graph.calculate_score()}.")
    print()

    # ---------------------------------------------------- NewGreedy ---------------------------------------------------------
    newGreedy_graph = gr.NewGreedy(stations_graph, the_map)
    print("newGreedy algorithm is running...")
    newGreedy_graph.run()

    print(f"newGreedy algorithm completed successfully with a score of {newGreedy_graph.graph.calculate_score()}.")
    print()    

    # -------------------------------------------------------- random --------------------------------------------------------
    # best_graph = None
    # best_score = 0
    # total_score = 0
    # for _ in range(RUNS):
    #     random_graph = randomize.random_assignment(stations_graph, the_map)
    #     if random_graph.calculate_score() > best_score:
    #         best_graph = random_graph
    #         best_score = random_graph.calculate_score()
    #     total_score += random_graph.calculate_score()
    # average_score = total_score / RUNS

    random_graph = randomize.random_assignment(stations_graph, the_map)
    print("Random algorithm is running...")
    print(f"Random algorithm completed successfully with a score of {random_graph.calculate_score()}.")

    print()
    # -------------------------------------------------------- output --------------------------------------------------------
    # Save graph to .csv file
    generate_output(reverseGreedy_graph.graph, output_file)
    print(f"See '{output_file}' for generated routes.")

    # Output info to file for personal use
    # generate_personal_output(best_graph, average_score, RUNS)

    # Visualize results on map
    if vis:
        from visualization import visualization
        
        print("Loading visualization...")
        visualization(the_map, reverseGreedy_graph.graph)
        print(f"Done! See 'test_{the_map}.png' for visualization.")


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
