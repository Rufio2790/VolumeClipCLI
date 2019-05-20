import os
import SimpleITK as sitk
import vtk
import transforms as trsf
import numpy as np


data_path = os.path.join(os.curdir, 'data')
scene_path = os.path.join(data_path, 'scene')
model_paths = os.path.join(scene_path, 'models')
surfaces = ['rh_pial.vtk', 'rh_white.vtk', 'lh_pial.vtk', 'lh_white.vtk']
image_path = os.path.join(scene_path, 'ref.nii.gz')
clipOutsideSurface = False
fillValue = 0
print(data_path)

# sitk read image
image = sitk.ReadImage(image_path)
image_lps = trsf.get_sitkImg_transform(image)

# vtk read image
reader = vtk.vtkNIFTIImageReader()
reader.SetFileName(image_path)
reader.Update()
vtkIm = reader.GetOutput()
print(vtkIm.GetOrigin())
print(vtkIm.GetSpacing())
print(vtkIm.GetExtent())
print(vtkIm.GetBounds())
vtkIm.SetSpacing([1., 1., 1.])

# vtkread surface
surf_reader = vtk.vtkPolyDataReader()
surf_reader.SetFileName(os.path.join(model_paths, surfaces[0]))
surf_reader.Update()
surf = surf_reader.GetOutput()

ras2ijk = trsf.get_ras2ijk(image)
surf_at_ijk = trsf.transform_poly_data(surf, ras2ijk)

# Convert model to stencil
polyToStencil = vtk.vtkPolyDataToImageStencil()
polyToStencil.SetInputData(surf_at_ijk)
polyToStencil.SetOutputSpacing(vtkIm.GetSpacing())
polyToStencil.SetOutputOrigin(vtkIm.GetOrigin())
polyToStencil.SetOutputWholeExtent(vtkIm.GetExtent())

writer = vtk.vtkImageWriter()
writer.SetInputData(polyToStencil.GetOutput())
# writer.SetFileName(os.path.join(data_path, 'poly2stencil.mha'))
writer.Update()

# Apply the stencil to the volume
stencilToImage = vtk.vtkImageStencil()
stencilToImage.SetInputData(vtkIm)
stencilToImage.SetStencilConnection(polyToStencil.GetOutputPort())
if clipOutsideSurface:
    stencilToImage.ReverseStencilOff()
else:
    stencilToImage.ReverseStencilOn()
stencilToImage.SetBackgroundValue(fillValue)
stencilToImage.Update()

clipedImg = stencilToImage.GetOutput()

writer = vtk.vtkImageWriter()
writer.SetInputData(clipedImg)
writer.SetFileName(os.path.join(data_path, 'results.mha'))
writer.Update()


print('ciao')


