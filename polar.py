from numpy import NaN
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
data_1_frame = pd.read_csv('./example-data4-1.csv')
data_2_frame = pd.read_csv("./example-data4-2.csv")
# data_3_frame = pd.read_csv("../Data-2/Capture-3/data3_updated.csv")
# data_4_frame = pd.read_csv("../Data-2/Capture-4/data4_updated.csv")


# print(data_1_frame)


angles_first_revolution = []
# print(angles_first_revolution)
angles_second_revolution = []
# angles_third_revolution = []
# angles_fourth_revolution = []


ranges_first_revolution = []
# range_first_revolution_lilst = []
# print(ranges_first_revolution)
ranges_second_revolution = []
# ranges_third_revolution = []
# ranges_fourth_revolution = []


# VTMS
# VTS


for index, row in data_1_frame.iterrows():
    if(row['Range(m)'] != NaN):
        if float(row['Range(m)']) < 3:
            angles_first_revolution.append(row['Angle'])
            ranges_first_revolution.append(row['Range(m)'])


for index, row in data_2_frame.iterrows():
    if(row['Range(m)'] != NaN):
        if float(row['Range(m)']) < 3:
            angles_second_revolution.append(row['Angle'])
            ranges_second_revolution.append(row['Range(m)'])


# fig1 = plt.figure()
# ax1 = fig1.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
# # ax1.set_yticks(np.arange(1, 1.3, 0.05))
# ax1.scatter(angles_first_revolution, ranges_first_revolution)
# plt.show()


ax1 = plt.subplot(121, polar=True)
ax2 = plt.subplot(122, polar=True)

# ax3 = plt.subplot(223, polar=True)
# ax4 = plt.subplot(224, polar=True)
ax1.scatter(angles_first_revolution, ranges_first_revolution, s=1)
ax2.scatter(angles_second_revolution, ranges_second_revolution, s=1)
# ax3.scatter(angles_third_revolution, ranges_third_revolution)
# ax4.scatter(angles_fourth_revolution, ranges_fourth_revolution)
plt.savefig('plot.png')

plt.show()
