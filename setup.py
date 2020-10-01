from setuptools import setup, find_packages
from os.path import splitext, basename
from glob import glob

setup(
    name="Copper", 
    package_dir={'': 'src'}, 
    packages=find_packages('src'), 
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')]
)
