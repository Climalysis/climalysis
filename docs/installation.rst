===============================================
Installation
===============================================

Climalysis can be accessed either directly from the GitHub repository or through the Python package.

GitHub Repository
-----------------

First, clone the repository::

    git clone https://github.com/Climalysis/climalysis.git

Next, navigate to the cloned repository and install the package::

    cd climalysis
    python setup.py install

Ensure you have Python 3.7 or higher installed on your system before installation.

Installing Python Package
-------------------------

You can also install Climalysis directly as a Python package::

    pip install climalysis

Dependencies
------------

Climalysis requires the following Python packages:

- numpy==1.23.5
- scikit_learn==1.2.1
- scipy==1.9.3
- setuptools==67.8.0
- statsmodels==0.13.5
- xarray==2023.3.0

These packages can be installed using pip by running the following command in your terminal::

    pip install -r requirements.txt
