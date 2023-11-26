import os
import pandas as pd
import random
read_directory = os.path.abspath('1. Iteration/Datapreprocessing/Splits')

test_directory = os.path.abspath('1. Iteration/Test-Train splits/Test')
train_directory = os.path.abspath('1. Iteration/Test-Train splits/Train')

split_percentage = 0.15

test_dict_processes = set()
test_dict = {}
train_dict = {}

#Reads a list of split eventlogs by connector, and generates a test and training dataset from these.
for filename in os.listdir(read_directory):
    f = os.path.join(read_directory, filename)
    df = pd.read_csv(f)
    
    grouped = df.groupby('RecordingId')

    #Files with more than 5 groups
    shuffleList = list(grouped.groups.keys())
    random.shuffle(shuffleList) #Shuffle recordings to pick random

    #Pick ~20% of records if number of records are > 5, otherwise pick 1 record
    numToPick = split_percentage * len(shuffleList) if len(shuffleList) > 5 else 1

    recordsToTest = []

    for recording in shuffleList: #Loop through recordings
        group = grouped.get_group(recording)
        processId = group.head(1)['ProcessId'].item() 
        if processId not in test_dict_processes: #Check that processId is not present in process id checkset
            if numToPick > 0: #If there are still available recordings to pick, pick one, remove from set
                recordsToTest.append(recording)
                numToPick -= 1
                test_dict_processes.add(processId)
            else: #If no more records are available, we can stop searching
                break
    
    recordsToTrain = [i for i in shuffleList if i not in recordsToTest and i not in test_dict.keys()] #Records to train are all records not in the test dict
    
    #Add this files test record to out dict. Remove from training out dict if duplicate
    for record in recordsToTest:
        if record not in test_dict.keys():
            test_dict[record] = grouped.get_group(record)
        if record in train_dict.keys():
            del train_dict[record]
    
    #Add this files training records to out dict.
    for record in recordsToTrain:
        train_dict[record] = grouped.get_group(record)
    
    