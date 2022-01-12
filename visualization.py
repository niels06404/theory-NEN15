from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd


### Nederland ###
ned = Basemap(projection='mill',
            llcrnrlat= 50.7,
            llcrnrlon= 3.2,
            urcrnrlat= 53.6,
            urcrnrlon= 7.3,
            resolution='h')

ned.drawcoastlines(linewidth=0.5)
ned.drawcountries()

df = pd.read_csv("data/StationsNationaal.csv")
x = list(df.x)
y = list(df.y)

for i in range(len(x)):
    xpt, ypt = ned(y[i], x[i])
    ned.plot(xpt, ypt, "ro", markersize=1)

plt.title('Nederland Intercities')
plt.savefig('plots/plot_res_h_N.png')

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