import os
import vtk
import SimpleITK as sitk
import clip
import transforms as trsf
import numpy as np


data_path = os.path.join(os.curdir, 'data')
scene_path = os.path.join(data_path, 'scene')
model_paths = os.path.join(scene_path, 'models')
surfaces = ['rh_pial.vtk', 'rh_white.vtk', 'lh_pial.vtk', 'lh_white.vtk']
image_path = os.path.join(scene_path, 'ref.nii.gz')
clipOutsideSurface = True
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

outputImageData = clip.clip_volume_with_surface_model(surf_at_ijk, vtkIm)

outputImageData.SetOrigin(vtkIm.GetOrigin())
outputImageData.SetSpacing(vtkIm.GetSpacing())

writer = vtk.vtkNIFTIImageWriter()
writer.SetInputData(outputImageData)
writer.SetFileName(os.path.join(data_path, 'resultsvtk.nii.gz'))
writer.Update()

out_image = sitk.ReadImage(os.path.join(data_path, 'resultsvtk.nii.gz'))
out_image.SetSpacing(image.GetSpacing())
out_image.SetDirection(image_lps[:3, :3].ravel())
out_image.SetOrigin(image_lps[:3, 3])

sitk.WriteImage(out_image, os.path.join(data_path, 'results.mha'))
meta_output = sitk.ReadImage(os.path.join(data_path, 'results.mha'))
sitk.WriteImage(out_image, os.path.join(data_path, 'nifti_result.nii.gz'), True)

print('ciao')


