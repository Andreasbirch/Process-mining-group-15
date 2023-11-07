import json
import math
import numpy as np

with open('conformance_checking.json') as json_file:
    data = json.load(json_file)
    arr = np.empty(shape=(51, 51))
    for process in data.keys():
        idx = int(process.split('_')[1])
        for subprocess in data[process]:
            subidx = int(subprocess.split('_')[1])
            val = round(data[process][subprocess]["average_trace_fitness"], 3)
            arr[idx][subidx] = val
    np.savetxt("conformance_checking_matrix.csv", arr, delimiter=",", fmt="%1.3f")