# pattern-generation-ni
The notebook `patternGeneration.ipynb` generates patterns in the form of JSON files which can be sent to microcontroller.
All instructions for this can be found in this notebook.

In the directory `./distinguishability` there are two python files: `staticPattern.py` and `dynamicPattern.py`.
These two files create a numpy array representing a respectively static of dynamic pattern in a `time x 6 x 6 x 2` grid. 
