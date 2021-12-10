from setuptools import setup, find_packages

setup(
    name='advent',
    version='0.1.0',
    packages=find_packages(include=['advent', 'advent.*'])
)