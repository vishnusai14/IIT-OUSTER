from matplotlib import pyplot as plt

contour_filter = [38, 37, 38, 36, 37, 36, 39,
                  35, 36, 37, 36, 40, 38, 37, 38, 37, 37, 37]
sobel_filter = [36, 36, 37, 36, 36, 35, 38, 35,
                35, 35, 36, 38, 36, 37, 36, 35, 35, 35]
canny_filter = [33, 34, 34, 33, 33, 35, 33,
                31, 33, 33, 34, 35, 34, 35, 33, 33, 33]

actual_dime = [40, 40, 40, 40, 40, 40, 40, 40,
               40, 40, 40, 40, 40, 40, 40, 40, 40, 40]


plt.plot(contour_filter, 'r')
plt.plot(sobel_filter, 'g')
plt.plot(canny_filter, 'b')
plt.plot(actual_dime, 'p')
plt.show()
