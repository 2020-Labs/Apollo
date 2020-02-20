import pandas as pd
import numpy as np


df = pd.read_excel('/work2/oppo.xls');


print(df.dtypes)
print(df)
# #从Excel读取出来的是整数，1900-1-1是整数1，而1970-1-1的整数是25569
#
# df.日期 = pd.to_datetime(df.日期 - 25569, unit='d')
# df.上班时间 = pd.to_datetime(df.上班时间, format='%H:%M:%S')
#
#
# df.下班时间 = pd.to_datetime(df.下班时间, format='%H:%M:%S')
#
# df['时长'] = df.下班时间 - df.上班时间
# df['时长'] = df['时长'].dt.seconds
# #df['时长'] = pd.to_datetime(df['时长'], unit='s').dt.time
# df['时长'] = df['时长']/3600
#
#
# df.上班时间 = df.上班时间.dt.time
# df.下班时间 = df.下班时间.dt.time
#
# print(df.dtypes)

#print(df.columns)

print('-'*10)
columns = []
print(df.columns[1])
for col in df.columns:
    #print(col.replace('\n',''))
    columns.append(col.replace('\n',''))

print(columns)

print('-'*10)
print(df.values)

values = []
for v in df.values:
    values.append(v)
    print('v:')
    print(v[6:])

print(df.values[0])

#print(values)

new_columns = columns[6:]

print('new columns: ')
print(new_columns)

new_values = []
for v in df.values:
    new_values.append(v[6:])

print('new values: ')
for v in new_values:
    print(v)


data = {}

