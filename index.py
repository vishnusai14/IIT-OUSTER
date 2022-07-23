
import cv2
from PIL import Image, ImageFilter
from more_itertools import difference
import numpy as np
from ouster import pcap
from ouster import client
import math
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.morphology import remove_small_objects

plt.ion()
metadata_path = '../Data-5/capture-1.json'
pcap_path = '../Data-5/capture-1.pcap'
with open(metadata_path, 'r') as f:
    metadata = client.SensorInfo(f.read())


length = 0
# config = client.SensorConfig()
# config.udp_port_lidar = 7502
# config.udp_port_imu = 7503
# config.operating_mode = client.OperatingMode.OPERATING_NORMAL
# client.set_config('os1-991939001247.local', config,
#                   persist=True, udp_dest_auto=True)


angles = []
ranges = []

ax1 = plt.subplot(111, polar=True)
ax1.set_ylim([0, 3])

source = pcap.Pcap(pcap_path, metadata)
previous_frame = []
difference_in_center = []
previous_centers = []
# source = client.Sensor('os1-991939001247.local')
while(1):
    centers = []

    scans = iter(client.Scans(source))
    try:
        scan = next(scans)
        print(scan)
        xyzlut = client.XYZLut(metadata)
        xyz = xyzlut(scan.field(client.ChanField.RANGE))
        for i in xyz:
            for j in i:
                length += 1
                angle = math.atan2(j[1], j[0])
                range = math.sqrt((j[0]*j[0]) + (j[1]*j[1]) + (j[2]*j[2]))
                if range < 2.5 and range != 0:
                    angles.append(angle)
                    ranges.append(range)
                if length == 16384:
                    # ax1.scatter([], [])
                    ax1.yaxis.grid(False)
                    ax1.xaxis.grid(False)
                    temp = ax1.scatter(angles, ranges)
                    plt.savefig('plot.png')
                    # img = cv2.imread('./plot.png')
                    # image = Image.open(r"./plot.png")
                    # image = image.convert("L")
                    # image = image.filter(ImageFilter.FIND_EDGES)
                    # image.save(r"plot-detect.png")
                    # image_detect = cv2.imread("./plot-detect.png")
                    # cv2.imshow('Image', image_detect)

                    rgb = cv2.imread('./plot.png')

                    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)

                    # threshold hue channel for purple tubes, value channel for blue tubes
                    thresh_hue = cv2.threshold(
                        hsv[..., 0], 127, 255, cv2.THRESH_BINARY)[1]
                    thresh_val = cv2.threshold(
                        hsv[..., 2], 200, 255, cv2.THRESH_BINARY)[1]
                    thresh = thresh_hue | thresh_val
                    thresh = cv2.morphologyEx(
                        thresh, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
                    h_kernel = np.zeros((11, 11), dtype=np.uint8)
                    h_kernel[5, :] = 1

                    v_kernel = np.zeros((11, 11), dtype=np.uint8)
                    v_kernel[:, 5] = 1

                    h_tubes = cv2.morphologyEx(
                        thresh, cv2.MORPH_OPEN, h_kernel, iterations=6)
                    v_tubes = cv2.morphologyEx(
                        thresh, cv2.MORPH_OPEN, v_kernel, iterations=7)

                    h_contours = cv2.findContours(h_tubes, cv2.RETR_LIST,
                                                  cv2.CHAIN_APPROX_SIMPLE)[0]
                    h_lines = np.zeros(thresh.shape, np.uint8)

                    for cnt in h_contours:
                        x, y, w, h = cv2.boundingRect(cnt)
                        y += int(np.floor(h / 2) - 4)
                        cv2.rectangle(h_lines, (x, y), (x + w, y + 8), 255, -1)

                    v_contours = cv2.findContours(v_tubes, cv2.RETR_LIST,
                                                  cv2.CHAIN_APPROX_SIMPLE)[0]
                    v_lines = np.zeros(thresh.shape, np.uint8)

                    for cnt in v_contours:
                        x, y, w, h = cv2.boundingRect(cnt)
                        x += int(np.floor(w / 2) - 4)
                        cv2.rectangle(v_lines, (x, y),
                                      (x + 32, y + h), 255, -1)

                    # combine horizontal and vertical lines
                    all_lines = h_lines | v_lines

                    xor = np.bool8(h_lines ^ v_lines)
                    removed = xor ^ remove_small_objects(xor, 350)

                    result = all_lines & ~removed * 255

                    cv2.imwrite('result.png', result)
                    image = cv2.imread("./result.png")
                    # image = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
                    prepared_frame = thresh
                    if previous_frame == []:
                        previous_frame = thresh
                    diff_frame = cv2.absdiff(
                        src1=previous_frame, src2=prepared_frame)
                    previous_frame = prepared_frame
                    kernel = np.ones((5, 5))
                    diff_frame = cv2.dilate(diff_frame, kernel, 1)
                    thresh_frame = cv2.threshold(
                        src=diff_frame, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]
                    contours, _ = cv2.findContours(
                        image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
                    # cv2.drawContours(image=image, contours=contours, contourIdx=-1,
                    #                  color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                    for i in contours:
                        M = cv2.moments(i)
                        x, y, w, h = cv2.boundingRect(i)
                        if M['m00'] != 0:
                            cx = int(M['m10']/M['m00'])
                            cy = int(M['m01']/M['m00'])
                            centers.append([cx, cy])
                            length = len(centers)
                            if previous_centers == []:
                                previous_centers = centers
                            for j in centers:
                                distance = math.sqrt(abs(j[0] - previous_centers[centers.index(j)][0]) + abs(
                                    j[1] - previous_centers[centers.index(j)][1]))
                                print(distance / 0.2)
                                cv2.putText(
                                    image, 'Velocity : ' + str(math.floor(distance/0.2)) + "cm/s", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.6, (36, 255, 12), 1)
                            previous_centers = centers
                            cv2.drawContours(image, [i], -1, (0, 255, 0), 2)
                            cv2.circle(image, (cx, cy), 7, (0, 0, 255), -1)

                    cv2.imshow('Image', image)
                    plt.pause(0.2)

                    # Reset the angles and ranges array
                    angles = []
                    ranges = []
                    temp.remove()
                    # temp2.remove()
                    # temp3.remove()
                    # Update the Plot
                    # print('One frame Done')
                    length = 0

    except StopIteration as e:
        break


# for packet in source:
#     if isinstance(packet, client.LidarPacket):

#         # Now we can process the LidarPacket. In this case, we access
#         # the measurement ids, timestamps, and ranges
#         encoder_count = packet.measurement_id
#         packet.field(client.ChanField)
#         encoder_ticks = []
#         # each one represesnt 44 ticks
#         for i in encoder_count:
#             encoder_ticks.append(i * 88)
#         length += len(encoder_ticks)
#         with open('../Data-3/Capture-2/data-2.csv', 'a') as f:
#             writer_obj = writer(f)
#             for i in range(0, len(encoder_ticks)):
#                 thetha_rad = 2*3.14*(1 - (encoder_ticks[i] / 90112))
#                 thetha = (180/3.14) * thetha_rad
#                 writer_obj.writerow(
#                     [encoder_ticks[i], thetha,  packet.timestamp[i]])
# print(length)
