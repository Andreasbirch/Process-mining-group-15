import pm4py
import pandas as pd
import glob
import os
import numpy as np
import confomance_matrix

class Logs:
    def __init__(self, df, name):
        self.df = df
        self.name = name

# Read all test logs files and put them in a list
def ReadTestAndTrainingLog():
    trainEventLogList = []
    testEventLogList = []

    # Read all training logs
    for filename in glob.glob(os.path.join('../Test-Train/Train', '*.csv')):
        log = pm4py.format_dataframe(pd.read_csv(filename), case_id='RecordingId',
                                           activity_key='Activity', timestamp_key='TimeStamp')
        filename = os.path.splitext(os.path.basename(filename))[0]
        
        df = Logs(log, filename)
        trainEventLogList.append(df)


    # Read all test logs
    for filename in glob.glob(os.path.join('../Test-Train/Test', '*.csv')):
        log = pm4py.format_dataframe(pd.read_csv(filename), case_id='RecordingId',
                                           activity_key='Activity', timestamp_key='TimeStamp')
        filename = os.path.splitext(os.path.basename(filename))[0]
        
        df = Logs(log, filename)
        testEventLogList.append(df)
        
    return trainEventLogList, testEventLogList

train, test = ReadTestAndTrainingLog()

performance = {}

for train_count, logTraining in enumerate(train):
    # Read data in csv file as dataframe, create event log.
    df = logTraining.df
    mask = df['ProcessId'] == df.ProcessId.unique()[0]
    df = df[mask]
    event_log = pm4py.format_dataframe(df, case_id='RecordingId', activity_key='Activity', timestamp_key='TimeStamp')
    performance[logTraining.name] = {}

    # Discover declare model
    declare_model = pm4py.discover_declare(event_log, case_id_key='RecordingId', activity_key='Activity', timestamp_key='TimeStamp')

    for test_count, logTesting in enumerate(test):
        # Read test data as csv
        df = logTesting.df
        mask = df['ProcessId'] == df.ProcessId.unique()[0]
        df = df[mask]
        test_log = pm4py.format_dataframe(df, case_id='RecordingId', activity_key='Activity', timestamp_key='TimeStamp')

        conformance = pm4py.conformance_declare(test_log, declare_model)
        performance[logTraining.name][logTesting.name] = conformance[0]['dev_fitness']

conformances_df = pd.DataFrame(performance)

confomance_matrix.CreateMatrix(conformances_df, "Declarative Conformance Matrix", False)