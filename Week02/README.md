# 机器学习训练营第0期（2020.12.23开课）
---
## 第2周：Python 性能调优指南
---
### 1. Python 性能调优指南 (上)
* Cython 运行：
  `python setup.py install`

### 2. Python 性能调优指南（下）
* Cython的作用：
  把Cython当作C使用；
  用作数据预处理
* cimport numpy as cnp: 直接调用numpy底层的C实现
* **The cnp.ndarray[double] syntax**
  
            %%cython -a

            cimport cython
            cimport numpy as cnp
            from libc.math cimport log

            @cython.boundscheck(False) # 不要生成执行边界检查的代码
            @cython.wraparound(False) # 不要生成执行环绕检查（负索引）的代码。
            cpdef shannon_entropy_v3(cnp.ndarray[double] p_x):
                cdef double res = 0.0
                cdef int n = p_x.shape[0]
                cdef int i
                for i in range(n):
                    res += p_x[i] * log(p_x[i])
                return -res
* 二维列表本质是指针的指针，它所存储的不一定是成块的
* **用行连续地址形式存储还是用列连续形式存储：**
            
            # 以列连续形式存储：
            cdef np.ndarray[double, ndim=2, mode='fortran'] arg = np.asfortranarray(matrix, dtype=np.float64)
            # 以行连续地址形式存储：
            cdef np.ndarray[double, ndim=2, mode='C'] arg = np.ascontiguousarray(matrix, dtype=np.float64)
            # 完整代码：
            %%cython 
            import numpy as np
            cimport numpy as np

            matrix = np.random.randn(10000, 2)

            cdef np.ndarray[double, ndim=2, mode='fortran'] arg = np.asfortranarray(matrix, dtype=np.float64)
* 把数据复制到Cython后才开始处理，速度有大提升：
  `cdef cnp.ndarray[int, ndim=2, mode='fortran'] data = np.asfortranarray(x, dtype=np.int32)` 其中前面到cnp中到int相当与np中的int32
* **注意Cpthon函数参数的传递模式（复制、移动等），尽量不要在Cpython中分配资源，即避免在C资源分配，在Cython资源释放。**（相关视频内容：week2下-01:22：05）

            # get_ind_cols是以复制的形式传递，前提是get_ind_cols是较小：
            cdef extern from "ind_cols.h":
                vector[long] get_ind_cols(double*, const long, const long)
            # 若get_ind_cols很大，则在get_ind_cols(double*, const long, const long)的参数中增加一个大的数组变量

* Eigen的使用（C++的一个库）：
  通用方法:numpy 使用 view 传递给 C;C 使用 openmp 或者Eigen。使用 Map 可以使用类似的 matlab 的语法。但是不支持 OpenMP。
  使用Eigen的好处是：可以同时使用SIMD。

* Pthon的GIL（全局解释器锁）：
  由于 Python 中 GIL(Python 2020) 的存在，使得本质上 python 只能用一个进程进行。

* ray(Python多进程库): 不能直接更改数组
* Cython 注意对类掌握

### 问题收集：
* 同名会冲突吗
  import numpy as np 
  cimport numpy as np

* double[::1] p_x 是什么意思：

              %%cython -a

              cimport cython
              from libc.math cimport log

              @cython.boundscheck(False)
              @cython.wraparound(False)
              def shannon_entropy_mv(double[::1] p_x): # ？？
                  cdef double res = 0.0
                  cdef int n = p_x.shape[0]
                  cdef int i
                  for i in range(n):
                      res += p_x[i] * log(p_x[i])
                  return -res
