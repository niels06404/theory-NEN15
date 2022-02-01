from visualization import histogram

# The results depend on the input data in the folder "output". This data should be generated first by running main.py.
# To get the exact same results as in the presentation, run: ... (seed = 77965460 dinsdag 1 feb 10000 runs, nationaal)

# Visual Nationaal without HillClimber, 10000 runs
histogram("Score distribution of different algorithms, without HillClimber, 10000 runs - Nationaal",
          "plots/hist10000nat", [1000, 7500], [0, 1800], hill=False)
histogram("Best scores of different algorithms, without HillClimber, 10000 runs - Nationaal",
          "plots/bar10000nat", [0, 7500], [0, 0], hill=False, barplot=True)

# Visual Nationaal with HillClimber, 10000 runs
histogram("Score distribution of different algortihms, with HillClimber, 10000 runs - Nationaal",
          "plots/hist10000nat_hc", [1000, 7500], [0, 1800], hill=True)
histogram("Best scores of different algorithms, with HillClimber, 10000 runs - Nationaal",
          "plots/bar100000nat_hc", [0, 7500], [0, 0], hill=True, barplot=True)
