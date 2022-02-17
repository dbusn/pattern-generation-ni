# pattern-generation-ni
The notebook `patternGeneration.ipynb` generates patterns in the form of JSON files which can be sent to microcontroller.
All instructions for this can be found in this notebook.

## Instruction on how to generate patterns:
### Prerequisites
To be able to execute the script, make sure that all the python dependencies are installed. This can be done by executing ```pip install -r requirements.txt``` if using pyenv or ```conda install --file requirements.txt``` if using conda/anaconda environemt. The ```requirement.txt``` file is located in the root directory of this repo.

### JSON generation:

To generate all the static patterns from Reed's paper execute the last cell in *patternGeneration.ipynb* notebook. This will output all json files in the directory the notebook is located in. For convenience all the patterns from the notebook are pre-generated and located in ``json/`` directory.
The only dynamic pattern included so far is UU. However, it is possible to generate any pattern once it is defined. To learn how to do that follow the UU example in the jupyter notebook and consult the [Reed paper](https://ieeexplore.ieee.org/abstract/document/8423203).

### Conversion to GIF
* **MacOS/Linux**:
Once all the json files are in json/ you can run ```convert2GIF.bash``` script to output all the GIFs into a gifs/ subdirectory. You can also see each GIF frame-by-frame by navigating to frames/"name-of-the-phoneme".
* **Windows:**
The same procedure applies but execute ```convert2GIF.ps1``` using powershell instead of the bash script.

### Distinguishability
In the directory `./distinguishability` there are two python files: `staticPattern.py` and `dynamicPattern.py`.
These two files create a numpy array representing a respectively static of dynamic pattern in a `time x 6 x 6 x 2` grid.
