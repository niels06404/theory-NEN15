from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd

def visualization(map, stations):
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
        lat, lon = stations[station]._x, stations[station]._y
        xpt, ypt = m(lon, lat)
        m.plot(xpt, ypt, "ro", markersize=1)

    xs = []
    ys = []
    xx, yy = m(4.872356, 52.338889)
    xs.append(xx)
    ys.append(yy)
    xx, yy = m(5.914166451, 52.96138763)
    xs.append(xx)
    ys.append(yy)
    m.plot(xs,ys, linewidth=0.5)

    plt.title(f'{map} Intercities')
    plt.savefig(f'plots/test_{map}.png')

### Nederland ###
# ned = Basemap(projection='mill',
#             llcrnrlat= 50.7,
#             llcrnrlon= 3.2,
#             urcrnrlat= 53.6,
#             urcrnrlon= 7.3,
#             resolution='h')

# ned.drawcoastlines(linewidth=0.5)
# ned.drawcountries()

# df = pd.read_csv("data/StationsNationaal.csv")
# x = list(df.x)
# y = list(df.y)

# for i in range(len(x)):
#     if i % 2 == 0:
#         col = "ro"
#     else:
#         col = "go"
#     xpt, ypt = ned(y[i], x[i])
#     ned.plot(xpt, ypt, col, markersize=1)

# plt.title('Nederland Intercities')
# plt.savefig('plots/plot_res_h_N.png')

### Holland ###
# hol = Basemap(projection='mill',
#             llcrnrlat= 51.7,
#             llcrnrlon= 4,
#             urcrnrlat= 53.1,
#             urcrnrlon= 5.3,
#             resolution='h')

# hol.drawcoastlines(linewidth=0.5)
# hol.drawcountries()

# df = pd.read_csv("data/StationsHolland.csv")
# x = list(df.x)
# y = list(df.y)

# for i in range(len(x)):
#     xpt, ypt = hol(y[i], x[i])
#     hol.plot(xpt, ypt, "ro", markersize=1.2)

# plt.title('Holland Intercities')
# plt.savefig('plots/plot_res_h_H.png')