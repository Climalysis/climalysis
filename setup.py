from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.5'
DESCRIPTION = 'A comprehensive toolkit for climate impact analysis.'
LONG_DESCRIPTION = 'A package that allows researchers, analysts, and climate enthusiasts to dissect complex climate data.'

# Setting up
setup(
    name="Climalysis",
    version=VERSION,
    author="Jake Casselman",
    author_email="<jake.w.casselman@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'numpy==1.23.5',
        'scikit_learn==1.2.1',
        'scipy==1.9.3',
        'setuptools==67.8.0',
        'statsmodels==0.13.5',
        'xarray==2023.3.0'
    ],
    keywords=['python', 'climate', 'analysis', 'climate analysis', 'climate data', 'impact analysis'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ]
)
