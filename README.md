# NIDMod - Network Integration and Diffusion Modeller
A package for implementing various data integration setups on complex networks, running network diffusion models, and analysing results.

Users are able to define their own data integration setups using indexing, comparisons, and clustering, and apply these to a set of networks to be integrated. Following this, users can define custom diffusion models and run them on the set of integrated networks. Lastly, the results of the models can be analysed. Each step in the process can also be executed independently, depending on users' needs.

The 'experiments' folder contains data and Jupyter notebooks for executing a number of social network experiments highlighting the impact of data integration decisions.

The package is built primarily on NetworkX 2.7.1 (https://networkx.org/), the Python Record Linkage Toolkit 0.14 (https://recordlinkage.readthedocs.io/en/latest/about.html), and NDlib 5.1.1 (https://ndlib.readthedocs.io/en/latest/).
