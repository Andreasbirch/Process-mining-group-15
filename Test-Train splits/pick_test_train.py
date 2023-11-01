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

    #Files with 2-5 recordings should have 1 recording taken
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

                break
    
    

print(test_dict.keys())
print(train_dict.keys())

    
    