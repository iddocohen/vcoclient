from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
     name='vcoclient',  
     version='0.1.4',
     scripts=['vcoclient.py'] ,
     author="Iddo Cohen",
     author_email="iddocohen@gmail.com",
     description="A simple VeloCloud Orchestrator (VCO) Python client",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/iddocohen/vcoclient",
     packages=find_packages(),
     python_requires=">=3.6",
     install_requires=requirements,
     classifiers=[
         "Programming Language :: Python :: 3.6",
         "Programming Language :: Python :: 3.7",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
