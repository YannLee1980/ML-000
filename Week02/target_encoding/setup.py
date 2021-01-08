from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

compile_flags = ['-std=c++11']
# linker_flags = ['-fopenmp']

module = Extension('encoding_cy',
                    ['encoding_cy.pyx'],
                    language='c++',
                    include_dirs=[numpy.get_include()],
                    extra_compile_args=compile_flags)

setup(
    name='encoding_cy',
    ext_modules=cythonize(module)
    )
