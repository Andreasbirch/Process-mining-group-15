import pm4py
import pandas as pd
import os
from pm4py.algo.filtering.log.variants import variants_filter
import json

train_directory = os.path.abspath('1. Iteration/Test-Train splits/Train')
test_directory = os.path.abspath('1. Iteration/Test-Train splits/Test')

result_dict = {}
for filename in os.listdir(train_directory):
    
    file = os.path.join(train_directory, filename)
    # load event log
    df = pd.read_csv(file)
    result_dict[filename[:-4]] = {} #Get process name
    
    event_log = pm4py.format_dataframe(df, case_id='RecordingId',
                                            activity_key='Activity', timestamp_key='TimeStamp')


    # Do process discovery Alpha Miner
    net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(event_log)
    #pm4py.view_petri_net(net, initial_marking, final_marking)

    #Compare each test log to the new model
    for testfilename in os.listdir(test_directory):

        testfile = os.path.join(test_directory, testfilename)
        testlog = pd.read_csv(testfile)
        result = pm4py.fitness_token_based_replay(event_log, net, initial_marking, final_marking)
        result_dict[filename[:-4]][testfilename[:-4]] = result
    
with open("conformance_checking.json", "w") as outfile: 
    json.dump(result_dict, outfile)