# pattern-generation-ni
**v1.1**

### Prerequisites
Make sure that all the packages listed in `requirements.txt` are installed. To do so, run ```pip install -r requirements.txt``` if you use pip and ```conda install --file requirements.txt``` if you use conda or miniconda. Keep in mind that in order to run code from the notebook you may need to install additional packages.

### Notebook
The `pattern-gen.ipynb` notebook contains code to run Simulated Annealing and get the best n patterns from a set.

### Pattern generation
Proceed to dynamicGeneration directory and run ```python dynamicGenerator.py -h``` to learn how to generate dynamic patterns.

List of parameters:
|Param        |Arg Type	|Description
|---        	|---	    |---
|n       	    |int      |Number of patterns to generate; required
|pathLike   	|None  	  |Generate path-like patterns
|static     	|None    	|Generate static patterns
|stridden   	|None   	|Generate stridden path-like patterns
|hanning     	|None   	|Generate patterns with hann function modulation
|block      	|None   	|Generate patterns with block modulation
|sawtooth   	|None   	|Generate patterns with sawtooth modulation
|numpy      	|None   	|Export patterns to a numpy array (default=False)
|jsonOnly   	|None     |Generate only json files
|cbor         |None     |Generate optional CBOR binaries

### Conversion to GIF
Patterns created by patternGenerator are automatically converted to gif files. If you want to keep only the json files, run dynamicGenerator with `--jsonOnly` flag
If you have JSON pattern files generated using an external tool, you may want to convert them to gif files. To do so:
* **MacOS/Linux**:
Once all the json files are in `json2gif` directory  run ```bash convert2Gif.bash``` script to output all the GIFs into a GIFS/ subdirectory.
* **Windows:**
The same procedure applies but execute ```.\convert2Gif.ps1``` using powershell.

### Versioning and branches:
There are two main branches: `main` and `unstable`. Please make sure to push your changes to unstable only and merge the branches only if you create a new stable release. 

This project follows these versioning rules:

**3**.0 - Major release, may include backwards-compatability breaking changes

3.**1** - Minor release, tweakes, fixes etc. without backwards-compatability breaking changes
