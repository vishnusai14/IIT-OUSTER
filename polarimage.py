import polarTransform
import matplotlib.pyplot as plt
import imageio
import numpy as np

verticalLinesImage = imageio.imread('../Data-2/Capture-1/images/extract1.jpg')

polarImage, ptSettings = polarTransform.convertToPolarImage(verticalLinesImage, initialRadius=30,
                                                            finalRadius=100, initialAngle=0,
                                                            finalAngle=2 * np.pi)

cartesianImage = ptSettings.convertToCartesianImage(polarImage)

plt.figure()
plt.imshow(polarImage, origin='lower')
plt.show()
