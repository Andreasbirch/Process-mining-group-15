import pm4py
import pandas as pd
import os
from pm4py.algo.filtering.log.variants import variants_filter

read_directory = os.path.abspath('1. Iteration/Test-Train splits/Train')
for filename in os.listdir(read_directory):
    print(filename)


for filename in os.listdir(read_directory):
    print("File is", filename)
    file = os.path.join(read_directory, filename)
    # load event log
    df = pd.read_csv(file)
    print(df.columns)
    event_log = pm4py.format_dataframe(df, case_id='RecordingId',
                                            activity_key='Activity', timestamp_key='TimeStamp')


    # Do process discovery Alpha Miner
    net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(event_log)
    pm4py.view_petri_net(net, initial_marking, final_marking)
