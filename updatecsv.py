import csv


# Read entire input file into a list.
with open('../Data-3/Capture-2/frame-44.csv', 'r', newline='') as inp:
    reader = csv.DictReader(inp)
    inputs = list(reader)

# Update input rows that match data in search.csv file.
with open('../Data-3/Capture-2/file0.csv', 'r', newline='') as sea:
    sea_reader = csv.DictReader(sea)
    for row in sea_reader:
        # print(row)
        angle = row['Angle']
        timestamp = row['TimeStamp']
        # print(timestamp)

        for input_ in inputs:
            # print(int(input_['Raw Timestamp']))
            if input_['Raw Timestamp'] == timestamp:  # Match?
                print('True')
                input_['Angle'] = angle
                # break

# Write updated input.csv data out into a file.
with open('../Data-3/Capture-2/data2_updated.csv', 'w', newline='') as outp:
    fieldnames = inputs[0].keys()
    writer = csv.DictWriter(outp, fieldnames)
    writer.writeheader()
    writer.writerows(inputs)

print('done')
