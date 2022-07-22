
import cv2
from PIL import Image, ImageFilter
from ouster import pcap
from ouster import client
import math
import matplotlib.pyplot as plt
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
# source = client.Sensor('os1-991939001247.local')
while(1):
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
                if range < 2.5:
                    angles.append(angle)
                    ranges.append(range)
                if length == 16384:
                    # ax1.scatter([], [])
                    temp = ax1.scatter(angles, ranges)
                    plt.savefig('plot.png')
                    img = cv2.imread('./plot.png')
                    image = Image.open(r"./plot.png")
                    image = image.convert("L")
                    image = image.filter(ImageFilter.FIND_EDGES)
                    image.save(r"plot-detect.png")
                    image_detect = cv2.imread("./plot-detect.png")
                    cv2.imshow('Image', image_detect)
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
