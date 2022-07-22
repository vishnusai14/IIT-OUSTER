from matplotlib import pyplot as plt
x_points = [0, 45, 90, 135, 180, 225, 270, 315]
y_points = [0, 1790, 0,  7648, 1640, 1987, 0, 0]

# creating the bar plot
plt.bar(x_points, y_points, color ='maroon',width = 1.5)
 
plt.xlabel("Angle of Rotation")
plt.ylabel("Range/ Distance")
plt.show()