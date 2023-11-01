import os
import pandas as pd
import random
read_directory = os.path.abspath('1. Iteration/Datapreprocessing/Splits')

test_directory = os.path.abspath('Test-Train splits/Test')
train_directory = os.path.abspath('Test-Train splits/Train')

split_percentage = 0.2

test_dict_processes = set()
test_dict = {}
train_dict = {}

for filename in os.listdir(read_directory):
    f = os.path.join(read_directory, filename)
    df = pd.read_csv(f)
    
    grouped = df.groupby('RecordingId')

    #Files with 2-5 recordings should have 1 recording taken, otherwise try and pick 20% of groups
    if grouped.ngroups <= 5 and grouped.ngroups > 1: #Files with 2-5 groups
        shuffleList = list(grouped.groups.keys())
        random.shuffle(shuffleList) #Shuffle recordings to pick random

        for recording in shuffleList: #Loop through recordings, add to test_dict if recording is not present
            group = grouped.get_group(recording)
            processId = group.head(1)['ProcessId'].item()
            if processId not in test_dict_processes: #Check that processId is not present in process id checkset
                #Add recording to test dict and process to checkset
                test_dict[recording] = grouped.get_group(recording) 
                test_dict_processes.add(processId)

                #Add the other recordings to the training dict (We assume recordingIds are unique and as such do no checking)
                shuffleList.remove(recording)
                for trainingRecording in shuffleList:
                    train_dict[trainingRecording] = grouped.get_group(trainingRecording)
                    shuffleList.remove(trainingRecording) #Instead of break?
    else: #Files with more than 5 groups
        shuffleList = list(grouped.groups.keys())
        random.shuffle(shuffleList) #Shuffle recordings to pick random

        numToPick = split_percentage * len(shuffleList) #Calculate how many picks correspond to 20% of total possible entries

        # recordsToRemove = []
        for recording in shuffleList: #Loop through recordings, add to test_dict if recording is not present
            group = grouped.get_group(recording)
            processId = group.head(1)['ProcessId'].item()
            if processId not in test_dict_processes: #Check that processId is not present in process id checkset
                if numToPick > 0:
                    numToPick -= 1
                    recordsToRemove.append(recording)
                    test_dict[recording] = grouped.get_group(recording)
                    test_dict_processes.add(processId)
                else:
                    train_list = [i for i in shuffleList if i not in recordsToRemove] #Create a list of original list of recordings but with test recordings removed
                    for train_record in train_list:
                        train_dict[train_record] = grouped.get_group(train_record)




# def printOcc(dict):
#     occDict = {}
#     for k in dict.keys():
#         if k in occDict.keys():
#             occDict[k] += 1
#         else:
#             occDict[k] = 1
#     print(occDict)      

print(len(test_dict.keys()))
print(len(train_dict.keys()))

# printOcc(test_dict)

    
    