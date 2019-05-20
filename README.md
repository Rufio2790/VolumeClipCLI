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