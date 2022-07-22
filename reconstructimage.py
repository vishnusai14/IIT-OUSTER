from contextlib import closing
from ouster import client, pcap
import numpy as np
import cv2
metadata_path = "../Data-2/Capture-1/capture-1.json"
pcap_path = "../Data-2/Capture-2/capture-2.pcap"
with open(metadata_path, 'r') as f:
    metadata = client.SensorInfo(f.read())
pcap_file = pcap.Pcap(pcap_path, metadata)

number_of_scan = 0
with closing(client.Scans(pcap_file)) as scans:
    for scan in scans:
        number_of_scan += 1
        # ref_field = scan.field(client.ChanField.REFLECTIVITY)
        # ref_val = client.destagger(pcap_file.metadata, ref_field)
        # ref_img = ref_val.astype(np.uint8)

        range_field = scan.field(client.ChanField.RANGE)
        range_val = client.destagger(pcap_file.metadata, range_field)
        ref_img = range_val.astype(np.uint8)

        filename = 'extract' + str(number_of_scan) + ".jpg"
        cv2.imwrite('../Data-2/Capture-1/images/'+filename, ref_img)
