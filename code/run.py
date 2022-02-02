import random
import sys
from code.algorithms import greedy as gr
from code.algorithms import hillclimber as hc
from code.algorithms import randomize as ra


def run_algorithm(algorithm, graph, the_map, RUNS, hill=False, seed=None):
    '''
    Runs the given algorithm.
    Returns best results, all scores and all graphs of the given algorithm.
    '''
    random.seed(seed)

    best_score = 0
    best_graph = None
    all_scores = []
    all_graphs = []

    print(f"{algorithm} algorithm is running {RUNS} times with seed {seed}...")

    for _ in range(RUNS):
        if algorithm == "Random":
            output_graph = ra.Random(graph, the_map)
        elif algorithm == "NewRandom":
            output_graph = ra.NewRandom(graph, the_map)
        elif algorithm == "Greedy":
            output_graph = gr.Greedy(graph, the_map)
        elif algorithm == "ReverseGreedy":
            output_graph = gr.ReverseGreedy(graph, the_map)
        elif algorithm == "RandomGreedy":
            output_graph = gr.RandomGreedy(graph, the_map)
        elif algorithm == "AdaptedGreedy":
            output_graph = gr.AdaptedGreedy(graph, the_map)
        else:
            return

        output_graph.run()

        if output_graph.graph.calculate_score() > best_score:
            best_graph = output_graph.graph
            best_score = output_graph.graph.calculate_score()

        all_graphs.append(output_graph.graph)
        all_scores.append(output_graph.graph.calculate_score())

    print(f"{algorithm} completed with a best score of {best_graph.calculate_score()} out of {RUNS} runs.", end="\n\n")

    sys.stdout = open(f"output/{algorithm}.csv", "w")
    print(f"{algorithm};", end="")
    print(*all_scores, sep=",")

    if hill:
        print(f"Running HillClimber on each of the generated {algorithm} algorithms with seed {seed}...", file=sys.__stdout__)
        best_hillclimber, scores_hillclimber = run_hillclimber(all_graphs, the_map)

        print(f"HillClimber completed with a best score of {best_hillclimber.calculate_score()}", file=sys.__stdout__,
              end="\n\n")

        print(f"{algorithm}Hill;", end="")
        print(*scores_hillclimber, sep=",")

    sys.stdout.close()
    sys.stdout = sys.__stdout__

    return best_graph, all_scores, all_graphs


def run_hillclimber(graphs, the_map, seed=None):
    '''
    Runs the HillClimber algorithm on an already completed graph.
    Returns best result and all scores of the HillClimber.
    '''
    random.seed(seed)

    best_score = 0
    best_hillclimber = None
    scores_hillclimber = []

    for graph in graphs:
        hillclimber = hc.HillClimber(graph, the_map)
        hillclimber.run()

        if hillclimber.graph.calculate_score() > best_score:
            best_hillclimber = hillclimber.graph
            best_score = hillclimber.graph.calculate_score()

        scores_hillclimber.append(hillclimber.graph.calculate_score())

    return best_hillclimber, scores_hillclimber
