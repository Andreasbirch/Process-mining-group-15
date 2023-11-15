import pm4py
import pandas as pd

# Read data in csv file as dataframe, create event log.
df = pd.read_csv("3. Iteration/Test-Train/Train/chrome.csv")
mask = df['ProcessId'] == df.ProcessId.unique()[0]
df = df[mask]
event_log = pm4py.format_dataframe(df, case_id='RecordingId', activity_key='Activity', timestamp_key='TimeStamp')

# Discover declare model
declare_model = pm4py.discover_declare(event_log, case_id_key='RecordingId', activity_key='Activity', timestamp_key='TimeStamp')

# Read test data as csv
df = pd.read_csv("3. Iteration/Test-Train/Test/chrome.csv")
mask = df['ProcessId'] == df.ProcessId.unique()[0]
df = df[mask]
test_log = pm4py.format_dataframe(df, case_id='RecordingId', activity_key='Activity', timestamp_key='TimeStamp')

conformance = pm4py.conformance_declare(test_log, declare_model)
print(conformance)