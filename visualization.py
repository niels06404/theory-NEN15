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
        lat_s, lon_s = stations[station]._x, stations[station]._y
        xpt_s, ypt_s = m(lon_s, lat_s)
        m.plot(xpt_s, ypt_s, "ro", markersize=2)
        for connection in stations[station]._connections_loc:
            xline = []
            yline = []
            xline.append(xpt_s)
            yline.append(ypt_s)
            lat_c, lon_c = stations[station]._connections_loc[connection]
            xpt_c, ypt_c = m(lon_c, lat_c)
            # print(f"{station}: {connection}")
            # print()
            xline.append(xpt_c)
            yline.append(ypt_c)
            m.plot(xline, yline, linewidth=0.5, color='b')

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