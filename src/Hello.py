import pandas as pd
import numpy as np

df = pd.DataFrame({'total_bill': [16.99, 10.34, 23.68, 23.68, 24.59],
                   'tip': [1.01, 1.66, 3.50, 3.31, 3.61],
                   'sex': ['Female', 'Male', 'Male', 'Male', 'Female'],
                   'briday': ['1990-3-2', '1990-3-2', '1990-3-2', '1990-3-2', '1990-3-2']})
# data type of columns
print(df.dtypes)
print("-" * 60);

df.briday = pd.to_datetime(df.briday, format="%Y-%m-%d")
# indexes
print(df.index)
print("-" * 60);

# return pandas.Index
print (df.columns)
print("-" * 60);

# each row, return array[array]
print(df.values)
print("-" * 60);
print(df)

#df.to_excel("d:\demo.xlsx")
print("\nDone.")