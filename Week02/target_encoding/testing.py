import pandas as pd
import numpy as np
import timeit
from encoding_py import target_mean_py
from encoding_cy import target_mean_cy


y = np.random.randint(2, size=(5000, 1))
x = np.random.randint(10, size=(5000, 1))
df = pd.DataFrame(np.concatenate([x, y], axis=1), columns=['x', 'y'])
data = np.array(df)
result_py = target_mean_py(data)
result_cy = target_mean_cy(data)
dif = np.linalg.norm(result_py - result_cy)

cy = timeit.timeit('target_mean_cy(data)', setup='import encoding_cy', number=100)
py = timeit.timeit('target_mean_py(data)', setup='import encoding_py', number=100)

print(f"cy={cy}, py={py}")
print(f'Cython is {py/cy}x faster.')
