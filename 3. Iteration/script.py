# This script provides the process discovery and conformance checking algorithms used to generate
# the matrix of conformance fitness values among the train models and the test logs

# import
import numpy as np
import pm4py as pm4py
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

class Logs:
    def __init__(self, df, name):
        self.df = df
        self.name = name

def ReadTestAndTrainingLog():
    """
    Reads all test and training log files

    Returns:
    A list of Dataframes for each event log for tests and training
    """
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



def ProcessDiscoveryConformanceChecking(TrainEventlog, TestEventLog, DiscoveryAlg, ConformanceAlg):
    """
    Main function for process discovery and conformance checking

    Generates a petri net from a train and test event log
    Applies a discovery algorithm determined by DiscoveryAlg, and a conformance checking method determined by ConformanceAlg
    
    Returns:
    A conformance value
    """
    # Get Training EventLog    
    if DiscoveryAlg == "IM":
        net, im, fm = pm4py.discover_petri_net_inductive(TrainEventlog)
    elif DiscoveryAlg == "HM":
        net, im, fm = pm4py.discover_petri_net_heuristics(TrainEventlog, dependency_threshold=0.5)
    elif DiscoveryAlg == "IMF":
        net, im, fm = pm4py.discover_petri_net_inductive(TrainEventlog, noise_threshold=0.5)
    
    if ConformanceAlg == "token":
        conformance = pm4py.fitness_token_based_replay(TestEventLog, net, im, fm)
        conformance = conformance['average_trace_fitness']
    elif ConformanceAlg == "alignments":
        conformance = pm4py.conformance.fitness_alignments(TestEventLog, net, im, fm)
        conformance = conformance['averageFitness']
    
    return conformance


def Performance(TrainingLogList, TestingLogList, discovery, conformance):
    """
    Generates a conformance matrix by a list of training logs and a list of testing logs,
    applying the ProcessDiscoveryConformanceChecking() function on every event log, 
    with a specifying parameter to select the discovery and conformance algorithm

    Returns:
    A dictionary containing the conformance matrix with a set of entries in the following order: {training:{test:conformance}}
    """
    performance = {}

    for count, logTraining in enumerate(TrainingLogList):
        print("Training log: " + str(count+1/(len(TrainingLogList)+1)*100) + "% done")
        performance[logTraining.name] = {}
        for logTesting in TestingLogList:
            performance[logTraining.name][logTesting.name] = ProcessDiscoveryConformanceChecking(logTraining.df, logTesting.df, discovery, conformance)
    
    return performance


def save_dict(dictionary, discAlg, confAlg):
    """
    Saves a conformance matrix dictionary to a csv file
    """
    df = pd.DataFrame()
    # For loop that iterate through the dictionary
    # Uses keys as column and names and inner keys as rows.
    # The values are added to the dataframe
    print(dictionary)
    for key in dictionary.keys():
        for inner_key in dictionary[key].keys():
            df.loc[key, inner_key] = dictionary[key][inner_key]
    
    # Save df to csv with index
    df.to_csv('output_' + str(discAlg) + '_'+ (confAlg)+ '.csv', index=True)
    

def CombineAll():
    """
    Reads test- and training event logs, 
    then applies every combination of discovery and conformance algorithms on the logs using the Performance() function
    
    Result:
    A conformance matrix is generated for each discovery and conformance algorithm, saved in .csv files
    """
    train, test = ReadTestAndTrainingLog()
    DiscAlgs = ["IM","IMF", "HM"]
    ConfAlgs = ["token","alignments"]
    for discAlg in DiscAlgs:
        for confAlg in ConfAlgs:
            performance = Performance(train, test, discAlg, confAlg)
            save_dict(performance, discAlg, confAlg)
            
    
CombineAll()



# Alg 3: Recommendation Algorithm. 
def RecommendationAlg(MinedModelList, LogForRecommendation, K, Conformance):
    maxConformance = set()

    for model in MinedModelList:
        c = Conformance(model, LogForRecommendation)
        maxConformance = maxConformance.union((model,np.mean(c)))
    
    listOfBestConformance = maxConformance.sort(key=lambda x: x[1], reverse=True)[:K]

    return listOfBestConformance




