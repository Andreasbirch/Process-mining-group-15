# Script used for the first iteration of the preprocessing of the data
# This includes labelling, splitting and saving the data

# Imports
import pandas as pd

# Reading the data
df = pd.read_csv("../../Recorded_Business_Tasks.csv")

# print the count of null values in each column
#print(df.isnull().sum())

# Find connectors in the data
connectors = df.ApplicationProcessName.value_counts()
#print(connector)


# Split the data into connector parts using dictionary
dfs = dict(tuple(df.groupby('ApplicationProcessName')))
#print(dfs.keys())
#print(dfs['OneDrive'])


# Generate new csv files for each connector
#for connector in dfs.keys():
#    dfs[connector].to_csv(connector + '.csv', index=False)