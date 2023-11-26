# Script used for the first iteration of the preprocessing of the data
# This includes labelling, splitting and saving the data

# Imports
import pandas as pd

# Reading the data
df = pd.read_csv("../../Initial.csv", sep=',')


# Create and populate activity column in df by concatenating the ApplicationProcessName and StepName
# if application process name is null, then populate with StepName
df['Activity'] = df['ApplicationProcessName'].fillna('') + df['StepName'].fillna('')

lst = []
for procid in df.ProcessId.unique():
    i = 0
    #print(procid)
    for connector in df.ApplicationProcessName.unique():
        if connector in df.loc[df['ProcessId'] == procid].ApplicationProcessName.unique():
            if connector != 'nan':
                i = i + 1
    lst.append(i)

# Count occurences of same number in list
from collections import Counter


# print connectors unquiue values and count, +1 only when there is a new recording id
for connector in df.ApplicationProcessName.unique():
    i = 0
    for recId in df.RecordingId.unique():
        if connector in df.loc[df['RecordingId'] == recId].ApplicationProcessName.unique():
            i = i + 1

# Find connectors in the data
connectors = df.ApplicationProcessName.unique()

# Remove nan from connectors
connectors = connectors[~pd.isnull(connectors)]


# print all unique ApplicationProcessName that are in each recording id
#for each connector, print all recording ids that contain that connector
dict = {}
for connector in connectors:
    dict[str(connector)] = df.loc[df['ApplicationProcessName'] == connector].RecordingId.unique()


# Create a csv file for each connector, and add all recording ids that contain that connector
for connector in dict:
    newDf = pd.DataFrame()
    for recId in dict[connector]:
        mask = df['RecordingId'] == recId
        tempDf = df[mask]
        newDf = pd.concat([newDf, tempDf])
    
    # Create a csv file for each connector stored in folder Splits
    newDf.to_csv("Splits/" + connector + ".csv", index=False)



# Create files on different processIds
for procId in df.ProcessId.unique():
    newDf = pd.DataFrame()
    mask = df['ProcessId'] == procId
    tempDf = df[mask]
    newDf = pd.concat([newDf, tempDf])
    newDf.to_csv("ProcessId/" + procId + ".csv", index=False)