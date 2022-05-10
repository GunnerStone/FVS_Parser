# FVS Parser
___
This repository allows for an easy to use Python API to help parse data from the outputs of the U.S. Forest Service's Forest Vegetation Simulator  ([FVS](https://www.fs.fed.us/fvs/)). 

<p align="center">
  <img src="Readme_Assets/readme_human_tabular.png">
</p>

The outputs from FVS come in human-readable tabular data like the image shown above. This lack of structure does not lend itself well to interfacing with data-science applications like Python, R, Excel, MongoDB, etc. This project aims to bridge that gap by extracting the data into a defined JSON object structure that can easily be extended for use in other applications. 


___

## User Features

The parser can extract the following top-level features:
- Calibtation Statistics
- CANFPROF
- CARBREPT
- DWDVLOUT
- FUELOUT

___

## Developer Features
- Add a `secrets.py` file in the `Configs` folder to store MongoDB information
    - `mongo_client_username = ***`
    - `mongo_client_password = ***`
    - `mongo_client_database = ***`
    - `mongo_client_collection = ***`
    - `mongo_client_name = mongodb://***`
- `utils/` and `scripts/` packages allows for easily contributing new functions without breaking others

___
## Installation
**REQUIREMENTS:** Windows
> Note: This was only tested on outputs of FVS Version 3856; 

FVS Parser requires the following software in order to run
- [Anaconda](https://www.anaconda.com/products/individual) to manage Python packages & environment

Install the conda environment by running `conda_env_installer/installer.bat` 
OR, for a manual installation, create the conda environment from `conda_env_installer/environment.yml` using the conda commands from [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)
___
## .out File Oranization

Place all .out files from an FVS run in the `outputs/` folder. 
This is where the program expects to find the .out files you want to parse. 


___
## Running your first parse

- Make sure your .out files are in the `outputs/` folder or use the test ones already there. 
- Setup your `secrets.py` to contain custom MongoDB information
- Run `driver.py`; This script will parse all information from the .out files in the `outputs/` folder and upload the scans to your MongoDB. 
___
## MongoDB Architecture & Organization

<p align="center">
  <img src="Readme_Assets/readme_mongodb_example.png">
</p>

The UID of each document is the name of the .out file. 
Each document is a collection of Treatments for a given .out file. 
Each Treatment is a collection of Iterations. 
Each Iteration is a collection of top-level features (CARBREPT, DWDVLOUT, etc). 
Each top-level feature is broken down by year. 
For a given year, you can check the stats of a low-level feature (Total Stand Carbon, Stand Dead, etc).



___
## Development

Want to contribute? Great!

Email [Gunner](https://github.com/GunnerStone) for collaborator access or fork and make your own version!
## License

MIT

