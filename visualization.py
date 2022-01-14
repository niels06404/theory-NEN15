from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import random

def visualization(map, stations, routes):
    if map == "Nationaal":
        m = Basemap(projection='mill',
            llcrnrlat= 50.7,
            llcrnrlon= 3.2,
            urcrnrlat= 53.6,
            urcrnrlon= 7.3,
            resolution='h')
    elif map == "Holland":
        m = Basemap(projection='mill',
            llcrnrlat= 51.7,
            llcrnrlon= 4,
            urcrnrlat= 53.1,
            urcrnrlon= 5.3,
            resolution='h')
    
    m.drawcoastlines(linewidth=0.5)
    m.drawcountries()

    for station in stations:
        # plotting stations on the map
        lat_s, lon_s = stations[station]._x, stations[station]._y
        xpt_s, ypt_s = m(lon_s, lat_s)
        m.plot(xpt_s, ypt_s, "ro", markersize=2)
        for connection in stations[station]._connections_loc:
            # plotting connections on the map
            r = random.random()
            b = random.random()
            g = random.random()
            xline = []
            yline = []
            xline.append(xpt_s)
            yline.append(ypt_s)
            lat_c, lon_c = stations[station]._connections_loc[connection][0]
            passed = stations[station]._connections_loc[connection][1]
            if passed:
                col = (r, g, b)
                # plt.plot(x, y, c=color)
                # col = "r"           
            else:
              col = "black"

            xpt_c, ypt_c = m(lon_c, lat_c)
            # print(f"{station}: {connection}")
            # print()
            xline.append(xpt_c)
            yline.append(ypt_c)
            m.plot(xline, yline, linewidth=0.5, color=col)

    

    plt.title(f'{map} Intercities')
    plt.savefig(f'plots/test_{map}.png')

#### hebben we nog nodig
#     if i % 2 == 0:
#         col = "ro"
#     else:
#         col = "go"