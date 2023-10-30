import pm4py
import pandas as pd
from pm4py.algo.filtering.log.variants import variants_filter


# load event log
event_log = pm4py.format_dataframe(pd.read_csv('../Datapreprocessing/Splits/Skype.csv'), case_id='RecordingId',
                                           activity_key='Activity', timestamp_key='TimeStamp')





print(event_log)
# Writing xes file
#pm4py.write_xes(event_log, "test.xes")


process_tree = pm4py.discover_process_tree_inductive(event_log)
bpmn_model = pm4py.convert_to_bpmn(process_tree)
pm4py.view_bpmn(bpmn_model)