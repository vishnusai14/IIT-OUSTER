import csv

csv_path = "../Data/Capture-4/pcap-4.csv"

with open(csv_path, 'r', newline='') as inp:
    reader = csv.DictReader(inp)
    inputs = list(reader)

input_to_be_added = []

for input in inputs:
    print(input[' RANGE (mm)'] != '0')
    if input[' RANGE (mm)'] != '0' and input['# TIMESTAMP (ns)'] != '0':
        input_to_be_added.append(input)

with open('../Data/Capture-4/pcap4_updated.csv', 'w', newline='') as outp:
    fieldnames = inputs[0].keys()
    writer = csv.DictWriter(outp, fieldnames)
    writer.writeheader()
    writer.writerows(input_to_be_added)
