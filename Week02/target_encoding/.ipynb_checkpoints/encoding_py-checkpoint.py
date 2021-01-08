import numpy as np
import pandas as pd
def target_mean_py(data):
    N = data.shape[0]
    result = np.zeros(data.shape[0])
    value_dict = dict()
    count_dict = dict()
    for i in range(N):
        x = data[i][0]
        value_dict[x] = value_dict.get(x, 0) + data[i][1]
        count_dict[x] = count_dict.get(x, 0) + 1
    for i in range(N):
        x = data[i][0]
        result[i] = (value_dict[x] - data[i][1]) / (count_dict[x] - 1)
    return result