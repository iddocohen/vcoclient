import setuptools
import sys

if sys.version_info.major < 3:
    print("vcoclient.py is only supported for python 3, please upgrade")
    sys.exit(1)

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setuptools.setup(
     name='vcoclient',  
     version='0.1.2',
     scripts=['vcoclient.py'] ,
     author="Iddo Cohen",
     author_email="iddocohen@gmail.com",
     description="A simple VeloCloud Orchestrator (VCO) Python client",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/iddocohen/vcoclient",
     packages=setuptools.find_packages(),
     install_requires=requirements,
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
