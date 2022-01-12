from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

m = Basemap(projection='mill',
            llcrnrlat= 50,
            llcrnrlon= 3,
            urcrnrlat= 54,
            urcrnrlon= 8)

# m.drawcoastlines()
# m.drawcountries()
# m.fillcontinents()
# m.bluemarble()
m.shadedrelief()


Alat, Alon = 52.63777924, 4.739722252
xpt, ypt = m(Alon, Alat)
m.plot(xpt, ypt, "ro")

plt.title('Basemap')
plt.savefig('plot.png')
