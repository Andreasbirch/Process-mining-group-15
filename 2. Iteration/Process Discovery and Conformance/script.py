# This script provides the process discovery and conformance checking algorithms used to generate
# the matrix of conformance fitness values among the train models and the test logs

# import
import numpy as np
import pm4py as pm4py
import pandas as pd
import glob
import os


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



# Alg 1:
# Main function for process discovery and conformance checking
def ProcessDiscoveryConformanceChecking(TrainEventlog, TestEventLog, DiscoveryAlg, ConformanceAlg):

    # Get Training EventLog    
    if DiscoveryAlg == "IM":
        net, im, fm = pm4py.discover_petri_net_inductive(TrainEventlog, noise_threshold=0.2)
    elif DiscoveryAlg == "HM":
        net, im, fm = pm4py.discover_petri_net_heuristics(TrainEventlog, dependency_threshold=0.5)
    elif DiscoveryAlg == "IMF":
        net, im, fm = pm4py.discover_petri_net_alpha(TrainEventlog)
    
    if ConformanceAlg == "token":
        conformance = pm4py.fitness_token_based_replay(TestEventLog, net, im, fm)
        conformance = conformance['average_trace_fitness']
    elif ConformanceAlg == "alignments":
        conformance = pm4py.conformance.fitness_alignments(TestEventLog, net, im, fm)
        conformance = conformance['averageFitness']
    
    return conformance


train, test = ReadTestAndTrainingLog() 



#Alg 2: By having the train and test lists containing all the train and test logs, and discovery and
#conformance checking algorithms as inputs, we iterate through the train and test logs lists
#and apply the first algorithm 1 on the logs (codes A.1, A.3). The returned value will be a
#dictionary containing the conformance fitness value among the train models and the test
#logs
def Performance(TrainingLogList, TestingLogList):
    discovery = "IM"
    conformance = "alignments"

    performance = {}

    for count, logTraining in enumerate(TrainingLogList):
        print("We are now at logTranining file number: " + str(count))
        performance[logTraining.name] = {}
        for logTesting in TestingLogList:
            performance[logTraining.name][logTesting.name] = ProcessDiscoveryConformanceChecking(logTraining.df, logTesting.df, discovery, conformance)
    
    return performance


performance = Performance(train[:2], test[:2])
print(performance)


def save_dict(dictionary):
	df = pd.DataFrame(dictionary)
    
	df.to_csv('output_all.csv', index=False)

	# Maximum value from each column
	max_values_df = pd.DataFrame(df.apply(max)).transpose()
	max_values_df.to_csv('max.csv', index=False)

save_dict(performance)

# Alg 3: Recommendation Algorithm. 
def RecommendationAlg(MinedModelList, LogForRecommendation, K, Conformance):
    maxConformance = set()

    for model in MinedModelList:
        c = Conformance(model, LogForRecommendation)
        maxConformance = maxConformance.union((model,np.mean(c)))
    
    listOfBestConformance = maxConformance.sort(key=lambda x: x[1], reverse=True)[:K]

    return listOfBestConformance




