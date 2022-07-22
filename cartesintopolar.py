import pandas as pd
import math
data_frame = pd.read_csv("../Data-4/frame-59.csv")

for index, row in data_frame.iterrows():
    x = row['Point:0']
    y = row['Point:1']
    z = row['Point:2']
    r = math.sqrt((x*x) + (y*y) + (z*z))
    thetha = math.atan2(y, x)
    phi = math.atan2(math.sqrt((x*x) + (y*y)), z)
    data_frame.loc[index, 'Angle'] = thetha
    data_frame.loc[index, 'Range(m)'] = r
    data_frame.loc[index, 'phi'] = (phi*180) / (2*math.pi)

data_frame.to_csv('example-data4-2.csv', index=False)

print('done')
