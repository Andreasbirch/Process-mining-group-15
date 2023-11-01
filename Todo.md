Prerequisites:

0. Read thesis
1. Fill out gaps in data specified by thesis
2. Find the combination of recordingid and processid (Written somewhere in thesis). Cool stuff about how they are combined
3. Find out how many processId for each recording
4. Try and look at everything separately, every caseId separately

DCR, Declaretive. Rum(Rule Miner) and Declare4py

# Overall plan

0. Start by checking how long each process takes, to see if there is a faster connector
1. Split data into test and training (p. 24)
2. Make a model for each process (Inductive, Heuristic, Declarative) using the training data
3. Take test data and run conformance checking (alignment and token replay) on each of the models
4. We now have results, a process that matches the training data the best
5. If we have more time we could boil down recommendations based on how fast they work

We can iterate on this.

# First iteration


- [] Data preprocessing.


- [] Modeling Alpha Alg.

- [] Conformance Checking, K-folds


Case ID = Recording ID
Activity = concatenate(Application/Process Name) (maybe)
Timestamp = Timestamp

Next.
Split according to connectors

