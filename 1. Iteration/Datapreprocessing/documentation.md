# Discoveries in the datapreprocessing part.
This document describes the changes that took place in the preprocessing part of our first iteration.

## Initial data set:
The initial data set was 'Initial.csv', in which a lot of mistakes were found.
These were cleaned to the best of our abilities, however also not touched to much
since this is the first iteration.


### List of columns: 
The format of the data includes the following columns: 
- StepId
- RecordingId
- ProcessId
- TimeStamp
- StepName
- StepDescription
- ApplicationProcessName
- ApplicationParentWindowName
- AutomationStep
- NextStepId
- label_EventName
- label_EventId

### Description of the Columns 
Columns in the dataset include:

Column Name | Description
------ | ------ 
StepId          | The number of the step within the recording. 
RecordingId     | ID of the recording.
ProcessId       | ID of the process, for which the recording was done. 
TimeStamp       | Timestamp of the step within the recoridng. 
StepName        | Name of the step. It is one of 19 different options, please see below for details. 
StepDescription         | More detailed description of the step. 
ApplicationProcessName  | Process Name, taken from the opened application.
ApplicationParentWindowName |  Parent Window Name, taken from the opened application.
AutomationCode         | A Script which could be used to automate that step. 
label_EventName         | Event name given by a person making the recording for the groupped steps. 
label_EventId           | ID of the group of steps, called an Event. 
------ 

### StepName
Step Name is a standardized name of the action taken by the user. It is one of the 19 values below, with the following distribution:
StepName | Frequency
----- | -----
Click UI element in window | 2504
Press button in window | 1406
Populate text field in window | 718
Select menu option in window | 404
Send keys | 387
Drag and drop UI element in window | 110
Select tab in window | 75
Set checkbox state in window | 44
Set drop-down list value in window | 20
Select radio button in window | 16
MouseAndKeyboard.SendKeys.FocusAndSendKeys | 15
Expand/collapse tree node in window | 9
Comment | 2
Move window | 2
Prepare a form for employees feedback | 0
Close window | 1
Resize window | 1
Locate the Notification and review it in Inbox of mailing app | 1
Get details of a UI element in window | 1


### Connectors
The results of this research is trough the usage of real event logs can recommend relevant connectors to the processes needed.
The table underneath states the unique connectors of our problem, their presence in a RecordingId, as well as their respective percentage.

| Unique Connectors   | Recordings where connector i present | Percentage % | 
| ------------- |:-------------:|:-------------:|
|   chrome      | 76         |      47.06 |
|   msedge      | 44           |    26.6    |
|   firefox     | 37           |    22.42   |
|   Teams       | 49           |    29.69   |
|   PBIDesktop  | 7           |     4.24    |
|   OUTLOOK     | 17           |    10.30   |
|   ApplicationFrameHost | 18   |   10.90   |
|   Ssms        | 9            |    5.45    |
|   CoollePDFConverter     | 4 |    2.42    |
|   OneDrive    | 3            |    1.81    |
|   SearchApp   | 18            |   10.90   |
|   explorer    | 9            |    5.45    |
|   EXCEL       | 2            |    1.21    |
|   Skype       | 5            |    3.03    |
|   ShellExperienceHost    | 8 |    4.84    |
|   cmd         | 1             |   0.60    |

Were are not going to be focusing on everything since the would overcomplicate our problem.
From the list of connectors we chose some to test

## Preprocessing
An essential part of Process Mining is the occurence of:
 `Case ID`, `TimeStamp` and `Activity`.
The original dataset contains CaseID and Timestamp:
In which CaseID = Recording ID, TimeStamp = TimeStamp.
However activity is very broadly mentioned in StepName e.g. "Press Buttom In Window",
this does not provide us with a clear enough definition in which we will be able to differentiate between the connectors,
thus we created a new column called Activity, which takes the Stepname and concatenate with ApplicationProcessName.
Hence we can differentiate between the different connectors.

The new dataset is stored in:
 `1. IterationData.csv`


# Splits
For now the new dataset have been split in unique .csv files in which is a connector is present in the recordingID,
then the entire RecordingId must be considered.

- [ ] Ask Andrea whether this is the correct assumption
- [ ] The Splits must then also