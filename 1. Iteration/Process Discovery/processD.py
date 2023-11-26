import pm4py
import pandas as pd
from pm4py.algo.filtering.log.variants import variants_filter


# load event log
df = pd.read_csv('../Datapreprocessing/Splits/chrome.csv')
mask = df['ProcessId'] == df.ProcessId.unique()[0]
df = df[mask]
event_log = pm4py.format_dataframe(df, case_id='RecordingId',
                                           activity_key='Activity', timestamp_key='TimeStamp')



# Writing xes file

# Do process discovery Alpha Miner
net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(event_log)
pm4py.view_petri_net(net, initial_marking, final_marking)


# conformance checking 
pn, im, fm = pm4py.discover_petri_net_inductive(event_log)
pm4py.view_petri_net(pn, im, fm)
print(pm4py.fitness_token_based_replay(event_log, pn, im, fm))