import argparse
from code.classes.stations_graph import StationsGraph
from code.run import run_algorithm, run_hill_climber

import pandas as pd

from visualization import histogram

# TODO: hillclimber in if regels 24 tm 27 
# TODO: kiezen welker algoritmes via command line [1h,2,3h,4,5], en hill aan of uit, default [1,2,3,4,5]
# TODO: run algorithm nog hill meegeven

def main(the_map, output_file, RUNS, visual):
    # Load data into the graph
    stations_graph = StationsGraph(f'data/Stations{the_map}.csv', f'data/Connecties{the_map}.csv')
    
    # Set up datafrom for visualization
    plot_df = pd.DataFrame()

    # ["AdaptedGreedy", "Greedy", "NewRandom", "RandomGreedy", "Random"]

    # -------------------------------------------------------- Random --------------------------------------------------------
    print(f"Random algorithm is running {RUNS} times...")
    best_random, scores_random, all_random_graphs = run_algorithm("Random", stations_graph, the_map, RUNS, seed=None)
    
    print(f"Random completed successfully with a best score of {best_random.calculate_score()} out of {RUNS} runs.", end="\n\n")
    
    plot_df["Random"] = pd.Series(scores_random).values

    # print("HillClimber algorithm is running on Random...")
    # best_hillclimber, scores_hillclimber_r = run_hill_climber(all_random_graphs, the_map)

    # plot_df["RandomHill"] = pd.Series(scores_hillclimber_r).values
    
    # ------------------------------------------------------- NewRandom ------------------------------------------------------
    print(f"NewRandom algorithm is running {RUNS} times...")
    best_new_random, scores_new_random, all_new_random_graphs = run_algorithm("NewRandom", stations_graph, the_map, RUNS, seed=None)
    
    print(f"NewRandom completed successfully with a best score of {best_new_random.calculate_score()} out of {RUNS} runs.", end="\n\n")
    
    plot_df["NewRandom"] = pd.Series(scores_new_random).values
    
    # print("HillClimber algorithm is running on NewRandom...")
    # best_hillclimber, scores_hillclimber_nr = run_hill_climber(all_new_random_graphs, the_map, seed=None)

    # plot_df["NewRandomHill"] = pd.Series(scores_hillclimber_nr).values
    
    # -------------------------------------------------------- Greedy --------------------------------------------------------
    print(f"Greedy algorithm is running {RUNS} times...")
    best_greedy, scores_greedy, all_greedy_graphs = run_algorithm("Greedy", stations_graph, the_map, RUNS, seed=None)
    
    print(f"Greedy completed successfully with a best score of {best_greedy.calculate_score()} out of {RUNS} runs.", end="\n\n")
    
    plot_df["Greedy"] = pd.Series(scores_greedy).values

    # print("HillClimber algorithm is running on Greedy...")
    # best_hillclimber, scores_hillclimber_g = run_hill_climber(all_greedy_graphs, the_map, seed=None)

    # plot_df["GreedyHill"] = pd.Series(scores_hillclimber_g).values
    
    # ----------------------------------------------------- RandomGreedy -----------------------------------------------------
    print(f"RandomGreedy algorithm is running {RUNS} times...")
    best_random_greedy, scores_random_greedy, all_random_greedy_graphs = run_algorithm("RandomGreedy", stations_graph, the_map, RUNS, seed=None)
    
    print(f"RandomGreedy completed successfully with a best score of {best_random_greedy.calculate_score()} out of {RUNS} runs.", end="\n\n")
    
    plot_df["RandomGreedy"] = pd.Series(scores_random_greedy).values

    # print("HillClimber algorithm is running on RandomGreedy...")
    # best_hillclimber_rag, scores_hillclimber_rag = run_hill_climber(all_random_greedy_graphs, the_map, seed=None)

    # plot_df["RandomGreedyHill"] = pd.Series(scores_hillclimber_rag).values
    
    # ----------------------------------------------------- ReverseGreedy ----------------------------------------------------
    # print(f"ReverseGreedy algorithm is running {RUNS} times...")
    # best_reverse_greedy, scores_reverse_greedy, all_reverse_greedy_graphs = run_algorithm("ReverseGreedy", stations_graph, the_map, RUNS, seed=None)
    
    # print(f"ReverseGreedy completed successfully with a best score of {best_reverse_greedy.calculate_score()} out of {RUNS} runs.", end="\n\n")
    
    # plot_df["ReverseGreedy"] = pd.Series(scores_reverse_greedy).values

    # print("HillClimber algorithm is running on ReverseGreedy...")
    # best_hillclimber_reg, scores_hillclimber_reg = run_hill_climber(all_reverse_greedy_graphs, the_map, seed=None)

    # plot_df["ReverseGreedy"] = pd.Series(scores_hillclimber_reg).values
    
    # ----------------------------------------------------- AdaptedGreedy ----------------------------------------------------
    print(f"AdapatedGreedy algorithm is running {RUNS} times...")
    best_adapted_greedy, scores_adapted_greedy, all_adapted_greedy_graphs = run_algorithm("AdaptedGreedy", stations_graph, the_map, RUNS, seed=None)
    
    print(f"AdaptedGreedy completed successfully with a best score of {best_adapted_greedy.calculate_score()} out of {RUNS} runs.", end="\n\n")
    
    plot_df["AdaptedGreedy"] = pd.Series(scores_adapted_greedy).values
    
    # print("HillClimber algorithm is running on AdaptedGreedy...")
    # best_hillclimber_ag, scores_hillclimber_ag = run_hill_climber(all_adapted_greedy_graphs, the_map, seed=None)

    # plot_df["AdaptedGreedyHill"] = pd.Series(scores_hillclimber_ag).values
    
    # -------------------------------------------------------- Output --------------------------------------------------------
    
    histogram("test", RUNS, the_map, hill=False)
    
    # Save graph to .csv file
    generate_output(best_adapted_greedy, output_file)
    print(f"See '{output_file}' for generated routes.")

    # Visualize results on map
    if visual:
        from visualization import visualization

        print("Loading visualization...")
        visualization(the_map, best_adapted_greedy)
        print(f"Done! See '{the_map}_routes.png' for visualization.")


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
    parser.add_argument("-V", help="Execute visualisation (default: True)", type=int, default=0, choices=[0, 1])

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.the_map, args.output_file, args.N, args.V)
