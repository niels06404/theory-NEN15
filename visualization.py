import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# with open("data/StationsHolland.csv", 'r') as file:
#     # Skip header line
#     next(file)
    
#     # Add station information to dictionary
#     x = []
#     y = []
#     station = []
#     stations = {}
    
#     for line in file:
#         info = line.strip().split(',')
#         x.append(info[1])
#         y.append(info[2])
#         station.append(info[0])
#         print(line[:-1])
#         stations[info[0]] = float(info[1]), float(info[2])

# print()
# for i in range(len(station)):
#     print(f"{station[i]}, x: {x[i]}, y: {y[i]}")
# print(stations)

df_nationaal = pd.read_csv("data/StationsNationaal.csv")
df_holland = pd.read_csv("data/StationsHolland.csv")

bbox = (df_nationaal.x.min()-0.1, df_nationaal.x.max()+0.1, df_nationaal.y.min()-0.1, df_nationaal.y.max()+0.1)
bbox_holland = (df_holland.x.min()-0.1, df_holland.x.max()+0.1, df_holland.y.min()-0.1, df_holland.y.max()+0.1)
# print(f"Nationaal: {bbox}")
# print(f"Holland: {bbox_holland}")

img = mpimg.imread("docs/Intercity stations.png")
imgplot = plt.imshow(img)
plt.show()


# img = mpimg.imread("docs/Intercity stations.png")
# fig, ax = plt.subplots(figsize = (8,6))
# ax.scatter(df_nationaal.y, df_nationaal.x, s=1, c="r")
# ax.set_xlim(bbox[2],bbox[3])
# ax.set_ylim(bbox[0],bbox[1])
# ax.imshow(img, zorder=0, extent = bbox, aspect= 'equal')
# imgplot = plt.imshow(img)
# plt.show()