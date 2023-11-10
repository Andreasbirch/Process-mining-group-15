# This script provides the process discovery and conformance checking algorithms used to generate
# the matrix of conformance fitness values among the train models and the test logs

# import
import numpy as np
import pm4py as pm4py
import pandas as pd
import glob
import os
import matplotlib
import matplotlib.pyplot as plt

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


# performance = Performance(train[:2], test[:2])
performance = {'Teams': {'Teams': 0.6811369925638111, 'CoollePDFConverter': 0.4444444444444444}, 'CoollePDFConverter': {'Teams': 0.369080003755136, 'CoollePDFConverter': 0.972972972972973}}
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

def CreateMatrix(dictionary, includeHeatmap = False):
    """
    Creates a matrix from a performance dictionary.
    Optionally generates heatmap png using matplotlib
    """
    df = pd.DataFrame(dictionary)

    #Save df to csv
    df.to_csv("conformance_matrix.csv", sep=",")

    if includeHeatmap:
        #Inspiration: https://matplotlib.org/stable/gallery/images_contours_and_fields/image_annotated_heatmap.html
        row_titles = df.columns.values.tolist()
        col_titles = df.index.tolist()
        data = df.values
        
        fig, ax = plt.subplots()
        im = ax.imshow(data)
        ax.set_yticks(np.arange(len(row_titles)), labels=row_titles)
        ax.set_xticks(np.arange(len(col_titles)), labels=col_titles)

        for i in range(len(row_titles)):
            for j in range(len(col_titles)):
                ax.text(j, i, data[i, j], ha="center", va="center", color="w")
                
        ax.set_title("Conformance matrix")
        fig.tight_layout()
        plt.savefig(fname="conformance_matrix_heatmap.png")
        plt.show()



CreateMatrix(performance, includeHeatmap=True)



