import os
import pandas as pd
read_directory = os.path.abspath('1. Iteration/Datapreprocessing/Splits')

test_directory = os.path.abspath('Test-Train splits/Test')
train_directory = os.path.abspath('Test-Train splits/Train')

split_percentage = 0.2

for filename in os.listdir(read_directory):
    f = os.path.join(read_directory, filename)
    df = pd.read_csv(f)
    
    test_fraction = df.sample(frac=split_percentage)
    train_fraction = df.drop(test_fraction.index)

    test_fraction.to_csv(os.path.join(test_directory, filename))
    train_fraction.to_csv(os.path.join(train_directory, filename))

    
    
    