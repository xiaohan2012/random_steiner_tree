# from distutils.core import setup, Extension
import os
from setuptools import setup, Extension

os.environ["CC"] = "g++"
os.environ["CXX"] = "g++"

core_module = Extension(
    'random_steiner_tree/interface',
    include_dirs=['/usr/include/python3.6m/'],
    library_dirs=['/lib/'],
    libraries=['boost_python36', 'boost_graph'],
    extra_compile_args=['-std=c++11', '-O2', '-Wall'],
    extra_link_args=['-Wl,--export-dynamic'],
    sources=['random_steiner_tree/interface.cpp']
)

setup(name='random_steiner_tree',
      version='0.1',
      description='Random Steiner tree sampling algorithm',
      url='http://github.com/xiaohan2012/random_steiner_tree',
      author='Han Xiao',
      author_email='xiaohan2012@gmail.com',
      license='MIT',
      packages=['random_steiner_tree'],
      ext_modules=[core_module],
      setup_requires=['pytest-runner'],
      tests_require=['pytest']
)
