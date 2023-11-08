# This script reads each file in Splits directory and split in test/train in 20/80 ratio based on the unique RecordingId

# Imports
import pandas as pd
import os
import random
import shutil
import sklearn.model_selection
import csv

# Method Read file in Splits directory
def readFiles():
    
    files = os.listdir("../Splits")
    # Read each file in Splits directory
    for file in files:
        df = pd.read_csv('../Splits/'+ str(file))
        
        #print(file)
        #print(len(df['RecordingId'].unique()))
        
        # Generate list of dataframes for each RecordingId
        list = []
        for recordingId in df['RecordingId'].unique():
            mask = df['RecordingId'] == recordingId
            df1 = df[mask]
            list.append(df1)
        
        # Split the list in 20/80 ratio generating test/train
        # Considering cmd has length of 1
        if len(list) > 1:
            train, test = sklearn.model_selection.train_test_split(list, test_size=0.2)
            
            newDf = pd.DataFrame()
            for dataframe in train:
                newDf = pd.concat([newDf, dataframe])
            
            # Create a csv file for each connector stored in folder Splits
            newDf.to_csv("../Test-Train/Train/" + file, index=False)
        
            newDf2 = pd.DataFrame()
            for dataframe in test:
                newDf2 = pd.concat([newDf2, dataframe])
            
            # Create a csv file for each connector stored in folder Splits
            newDf2.to_csv("../Test-Train/Test/" + file, index=False)




    return list

lst=readFiles()

