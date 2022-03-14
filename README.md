# pattern-generation-ni

### Prerequisites
Make sure that all the packages listed in `requirements.txt` are installed. To do so, run ```pip install -r requirements.txt``` if you use pip and ```conda install --file requirements.txt``` if you use conda or miniconda. Keep in mind that in order to run code from the notebook you may need to install additional packages.

### Notebook
In the `pattern-gen.ipynb` notebook all the code is stored, including setup code. You can simply run that for most applications.

### Dynamic pattern generation
Proceed to dynamicGeneration directory and run ```python dynamicGenerator.py -h``` to learn how to generate dynamic patterns.

#### Conversion to GIF
If you have JSON pattern files generated using an external tool, you may want to convert them to gif files. To do so:
* **MacOS/Linux**:
Once all the json files are in json/  run ```convert2GIF.bash``` script to output all the GIFs into a GIFS/ subdirectory.
* **Windows:**
The same procedure applies but execute ```convert2GIF.ps1``` using powershell instead of the bash script.
