import copy


def visualization(the_map, graph):
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap

    if the_map == "Nationaal":
        fonts = "xx-small"
        col = ["#a8d5e2", "#f9a620", "#ffd449", "#548c2f", "#104911", "#c84630", "#00916e", "#a4036f", "#7a6c5d", "#19297c",
               "#172a3a", "#8c93a8", "#a9f8fb", "#f0c808", "#96e6b3", "#f51aa4", "#561d25", "#ff3864", "#ffdab9", "#72b01d"]
        linew = [2 for _ in range(20)]

        m = Basemap(projection='mill',
                    llcrnrlat=50.7,
                    llcrnrlon=3.2,
                    urcrnrlat=53.6,
                    urcrnrlon=7.3,
                    resolution='h')
    else:
        fonts = "medium"
        col = ["#979af0", "#C20208", "#69CC66", "#3a3d91", "#ded837", "#a7dbda", "#BF1BC4"]
        linew = [6, 5.2, 4.4, 3.6, 2.8, 2, 1.2]

        m = Basemap(projection='mill',
                    llcrnrlat=51.7,
                    llcrnrlon=4,
                    urcrnrlat=53.1,
                    urcrnrlon=5.3,
                    resolution='h')

    m.drawcoastlines(linewidth=0.5)
    m.drawcountries()

    # Plotting routes on the map
    routes = graph.routes.values()
    traject = 1
    for route in routes:
        xs_r, ys_r = ([] for _ in range(2))
        for i in range(len(route.stations)):
            xs_r.append(route.stations[i]._x)
            ys_r.append(route.stations[i]._y)
        xline_r, yline_r = m(ys_r, xs_r)
        m.plot(xline_r, yline_r, color=col[traject - 1], linewidth=linew[traject - 1], label=f"Traject {traject}")
        traject += 1

    # Plotting unused connections on the map
    unused_connections = graph.get_unused_connections()
    unused_connections = cleanup_connections(unused_connections)
    for connection in unused_connections:
        xs_uc = []
        ys_uc = []
        # for station in connection:
        xs_uc.append(graph.stations[connection[0]]._x)
        ys_uc.append(graph.stations[connection[0]]._y)
        xs_uc.append(graph.stations[connection[1]]._x)
        ys_uc.append(graph.stations[connection[1]]._y)
        xline_uc, yline_uc = m(ys_uc, xs_uc)
        m.plot(xline_uc, yline_uc, "k", linestyle="--", dashes=(5, 5), linewidth=0.6)

    # Plotting stations on the map
    stations = list(graph.stations.keys())
    for station in stations:
        lat_s, lon_s = graph.stations[station]._x, graph.stations[station]._y
        xpt_s, ypt_s = m(lon_s, lat_s)
        m.plot(xpt_s, ypt_s, "ro", markersize=2)

    plt.title(f'{the_map} Intercities')
    plt.legend(loc=2, fontsize=fonts)
    plt.savefig(f'plots/{the_map}_routes.png')


def histogram(title, RUNS, the_map, hill=False):
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns

    plot_df = pd.DataFrame()
    x = [] # NOTE: wat te doen als hill TRUE
  
    for algorithm in ["AdaptedGreedy", "Greedy", "NewRandom", "RandomGreedy", "Random"]:
        with open(f"output/{algorithm}.csv", "r") as file:
            if hill:
                next(file)

            for line in file:
                line2 = line.split(";")
                
                list_items = line2[1].strip().split(",")
                int_list_items = list(map(float, list_items))

                x.append(max(int_list_items))
                plot_df[line2[0]] = pd.Series(int_list_items).values
                if not hill:
                    break

    sns.set_theme()
    sns.set_context("poster")
    p = sns.histplot(data=plot_df, kde=True, bins=80)
    p.set_title(f"{title}") # NOTE: bij command line of als input title meegeven
    p.set_xlabel("Score")
    plt.xlim([1500, 7500]) # min(all.) - 200 # NOTE: geen goeie verhouding met holland
    # plt.ylim([0, 2000]) # NOTE: af laten hangen van hoe groot RUNS is
    # # plt.savefig("plots/test_random.png")
    plt.show()

    plt.clf()
    
    sns.set_context("talk")
    
    y = ["AdaptedGreedy", "Greedy", "NewRandom", "RandomGreedy", "Random"]
    if hill:
        y = ["AdaptedGreedyHill", "GreedyHill", "NewRandomHill", "RandomGreedyHill", "RandomHill"]

    q = sns.barplot(x=x, y=y)
    q.set_title(f"Best scores for different algorithms without hillclimber ({RUNS} runs) - {the_map}")
    # q.set_title("Best scores for different algorithms without hillclimber (10000 runs) - {the_map}")
    plt.xlim([0, 7500]) # NOTE: AFHANKELIJK VAN MAP
    plt.savefig("plots/barplot.png")
    plt.show()


def cleanup_connections(connections):
    connections1 = copy.deepcopy(connections)
    for connection in connections:
        if (connection[1], connection[0]) in connections1:
            connections1.pop(connections1.index(connection))
    return connections1
