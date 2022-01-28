import argparse
import random
import sys
from code.algorithms import greedy as gr
from code.algorithms import hillclimber as hc
from code.algorithms import randomize
from code.algorithms import randomize2 as r2
from code.classes.stations_graph import StationsGraph

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main(the_map, output_file, RUNS, visual):
    # Load data into the graph
    stations_graph = StationsGraph(f'data/Stations{the_map}.csv', f'data/Connecties{the_map}.csv')
    
    # Set up datafrom for visualization
    plot_df = pd.DataFrame(columns=["Random", "NewRandom", "Greedy", "RandomGreedy", "AdaptedGreedy"])
    # plot_df = pd.DataFrame(columns=["AdaptedGreedy", "HillClimber"])

    # -------------------------------------------------------- Random --------------------------------------------------------
    random.seed()

    print(f"Random algorithm is running {RUNS} times...")
    best_score_random = 0
    scores_random = []
    
    for _ in range(RUNS):
        random_graph = randomize.random_assignment(stations_graph, the_map)

        if random_graph.calculate_score() > best_score_random:
            best_random = random_graph
            best_score_random = random_graph.calculate_score()
        
        scores_random.append(random_graph.calculate_score())

    print(f"Random completed successfully with a best score of {best_score_random} out of {RUNS} runs.")
    print()
    
    plot_df["Random"] = pd.Series(scores_random).values

    # ------------------------------------------------------- NewRandom ------------------------------------------------------
    random.seed()

    print(f"NewRandom algorithm is running {RUNS} times...")
    best_score_new_random = 0
    scores_new_random = []

    for _ in range(RUNS):
        new_random = r2.NewRandom(stations_graph, the_map)
        new_random.run()
        
        if new_random.graph.calculate_score() > best_score_new_random:
            best_new_random = new_random
            best_score_new_random = new_random.graph.calculate_score()

        scores_new_random.append(new_random.graph.calculate_score())

    print(f"NewRandom completed successfully with a best score of {best_score_new_random} out of {RUNS} runs.")
    print()
    
    plot_df["NewRandom"] = pd.Series(scores_new_random).values


    # -------------------------------------------------------- Greedy --------------------------------------------------------
    random.seed()
    
    print(f"Greedy algorithm is running {RUNS} times...")
    best_score_greedy = 0
    scores_greedy = []
    
    for _ in range(RUNS):
        greedy = gr.Greedy(stations_graph, the_map)
        greedy.run()
        
        if greedy.graph.calculate_score() > best_score_greedy:
            best_greedy = greedy
            best_score_greedy = greedy.graph.calculate_score()
        
        scores_greedy.append(greedy.graph.calculate_score())
    
    print(f"Greedy completed successfully with a best score of {best_score_greedy} out of {RUNS} runs.")
    print()
    
    plot_df["Greedy"] = pd.Series(scores_greedy).values

    # ----------------------------------------------------- RandomGreedy -----------------------------------------------------
    random.seed()
    
    print(f"RandomGreedy algorithm is running {RUNS} times...")
    best_score_random_greedy = 0
    scores_random_greedy = []
    
    for _ in range(RUNS):
        random_greedy = gr.RandomGreedy(stations_graph, the_map)
        random_greedy.run()
        
        if random_greedy.graph.calculate_score() > best_score_random_greedy:
            best_random_greedy = random_greedy
            best_score_random_greedy = random_greedy.graph.calculate_score()
        
        scores_random_greedy.append(random_greedy.graph.calculate_score())
    
    print(f"RandomGreedy completed successfully with a best score of {best_score_random_greedy} out of {RUNS} runs.")
    print()
    
    plot_df["RandomGreedy"] = pd.Series(scores_random_greedy).values

    # ----------------------------------------------------- ReverseGreedy ----------------------------------------------------
    random.seed()
    
    print(f"ReverseGreedy algorithm is running {RUNS} times...")
    best_score_reverse_greedy = 0
    scores_reverse_greedy = []
    
    for _ in range(RUNS):
        reverse_greedy = gr.ReverseGreedy(stations_graph, the_map)
        reverse_greedy.run()
        
        if reverse_greedy.graph.calculate_score() > best_score_reverse_greedy:
            best_reverse_greedy = reverse_greedy
            best_score_reverse_greedy = reverse_greedy.graph.calculate_score()
        
        scores_reverse_greedy.append(reverse_greedy.graph.calculate_score())
    
    print(f"ReverseGreedy completed successfully with a best score of {best_score_reverse_greedy} out of {RUNS} runs.")
    print()

    # ----------------------------------------------------- AdaptedGreedy ----------------------------------------------------
    random.seed()
    
    print(f"AdaptedGreedy algorithm is running {RUNS} times...")
    best_score_adapted_greedy = 0
    scores_adapted_greedy = []
    all_adapted_greedy = []
    
    for _ in range(RUNS):
        adapted_greedy = gr.AdaptedGreedy(stations_graph, the_map)
        adapted_greedy.run()
        
        if adapted_greedy.graph.calculate_score() > best_score_adapted_greedy:
            best_adapted_greedy = adapted_greedy
            best_score_adapted_greedy = adapted_greedy.graph.calculate_score()
        all_adapted_greedy.append(adapted_greedy.graph)
        scores_adapted_greedy.append(adapted_greedy.graph.calculate_score())
    
    print(f"AdaptedGreedy completed successfully with a best score of {best_score_adapted_greedy} out of {RUNS} runs.")
    print()
    
    plot_df["AdaptedGreedy"] = pd.Series(scores_adapted_greedy).values

    # ------------------------------------------------------ HillClimber -----------------------------------------------------
    random.seed()
    
    print("HillClimber algorithm is running ...")
    scores_hillclimber = []
    
    for graph in all_adapted_greedy:
        hillclimber = hc.HillClimber(graph, the_map)
        hillclimber.run()
        scores_hillclimber.append(hillclimber.graph.calculate_score())   

    print(f"HillClimber completed successfully with a score of {hillclimber.graph.calculate_score()}.")
    print()
    
    plot_df["HillClimber"] = pd.Series(scores_hillclimber).values

    # -------------------------------------------------------- Output --------------------------------------------------------
    
    sns.set_theme()
    sns.set_context("poster")
    p = sns.histplot(data=plot_df, kde=True, bins=80)
    p.set_title(f"AdaptedGreedy vs. HillClimber ({RUNS} runs) - National")
    p.set_xlabel("Score")
    
    plt.show()
    
    # Save graph to .csv file
    generate_output(hillclimber.graph, output_file)
    print(f"See '{output_file}' for generated routes.")

    # Visualize results on map
    if visual:
        from visualization import visualization

        print("Loading visualization...")
        visualization(the_map, hillclimber.graph)
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
    parser.add_argument("-V", help="Execute visualisation (default: True)", type=int, default=1, choices=[0, 1])

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provided arguments
    main(args.the_map, args.output_file, args.N, args.V)
