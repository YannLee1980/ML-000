# distutils: language=c++
import numpy as np
cimport numpy as cnp
from libcpp.map cimport map
from libcpp.vector cimport vector

cpdef target_mean_cy(x):
    cdef cnp.ndarray[int, ndim=2, mode='fortran'] data = np.asfortranarray(x, dtype=np.int32)
    cdef int N = data.shape[0]
    cdef map[int, int] ValueMap
    cdef map[int, int] CountMap
    cdef int i
    cdef int j
    cdef cnp.ndarray[double] result = np.zeros(N)
    for i in range(N):
        x = data[i,0]
        ValueMap[x] += data[i, 1]
        CountMap[x] += 1
    for j in range(N):
        x = data[j,0]
        result[j] = (ValueMap[x] - data[j,1]) / (CountMap[x] - 1)
    return result