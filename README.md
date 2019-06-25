# Command line Clip Module for Niguarda Hospital
*author: Davide Scorza*

This is a cmd line module to clip a volume from a vtk surface model

### Command line

To check the help: 
`python simple_clip -h`

Mandatory inputs: 
`python simple_clip -i=path_to_image -s=path_to_surface -o=output_path`

Complete call:
`python simple_clip -i=path_to_image -s=path_to_surface -o=output_path, 
-t=path_to_transform, --inside=True`

Parameters: 
*  **-i** -> path to the image
*  **-s** -> path to the surface to use
*  **-o** -> output file
*  **-t** -> transform to be applied to the surface model BEFORE performing the 
         CLIP. It is assumed that the model is in RAS space, while the transform 
         is passed in ITK LPS space.
*  **--inside** -> clip inside or outside the volume


# Installing Instructions

This module is a Python command line interface, therefore it requires python 3 installed in the system with some specific packages in order to be used correctly. 
Anaconda / Miniconda is a package manager from which it is possible to download the python interpreter as well as the packages to be installed. 

* Download [miniconda](https://docs.conda.io/en/latest/miniconda.html) for your system, with Python 3

_An alternative solution could be through the official python and by using pip._ 

Module Dependencies: 
* numpy
* SimpleITK
* vtk
* nibabel

The dependencies to run the application can be found in the file `environment_py3.yml`

Miniconda allows to create virtual environment ([conda environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)), which are very useful when you are working on projects with different dependencies of the same package or different python versions. 
If you plan to work on the same python version, you won't probably need any virtual environment and you can manually install on your base python the required packages with these commands: 

Run in your terminal: 

* `conda install -c simpleitk simpleitk` -> [sitk](https://anaconda.org/simpleitk/simpleitk)
* `conda install -c anaconda vtk`    -> [vtk](https://anaconda.org/anaconda/vtk)
* `conda install numpy`
* `conda install -c conda-forge nibabel` -> [nibabel](https://anaconda.org/conda-forge/nibabel)

If you plan to use a virtual environment, you can run: 
* `conda env create -f environment_py3.yml`

In this case, the dependencies will be automatically installed in a virtual environment named _CicoClip_.
You can list the available environments in the system by running in a terminal: 
* `conda env list`

With virtual environment, you must guarantee that the python interpreter used is the correct one (where the dependencies have been installed). 
The environment interpreter are usually stored in a folder like /user/miniconda/envs/env_name/python
