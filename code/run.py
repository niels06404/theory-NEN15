import random
import sys
from code.algorithms import greedy as gr
from code.algorithms import hillclimber as hc
from code.algorithms import randomize as ra


def run_algorithm(algorithm, graph, the_map, RUNS, hill=False, seed=None):
    random.seed(seed)
    
    best_score = 0
    best_graph = None
    all_scores = []
    all_graphs = []
    
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
        else: return
        
        output_graph.run()
    
        if output_graph.graph.calculate_score() > best_score:
            best_graph = output_graph.graph
            best_score = output_graph.graph.calculate_score()
        
        all_graphs.append(output_graph.graph)
        all_scores.append(output_graph.graph.calculate_score())
    
    sys.stdout = open(f"output/{algorithm}.csv", "w")
    print(f"{algorithm};", end="")
    print(*all_scores, sep=",")

    if hill:   
        best_hillclimber, scores_hillclimber = run_hill_climber(all_graphs, the_map)

        print(f"{algorithm}Hill;", end="")
        print(*scores_hillclimber, sep=",")
    
    sys.stdout.close()
    sys.stdout = sys.__stdout__

    return best_graph, all_scores, all_graphs

def run_hill_climber(graphs, the_map, seed=None):
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
