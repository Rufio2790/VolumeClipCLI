"""
Read and Write Utility script for surfaces and images.
It collects function to read and write surface with VTK (especially) and ITK (sometimes). Functions here are mainly
vtk filters wrappers.
"""

import vtk
import SimpleITK as sitk

def read_vtk_nifti_image(image_path):

    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(image_path)
    reader.Update()
    return reader.GetOutput()


def write_vtk_nifti_image(image, image_path):

    writer = vtk.vtkNIFTIImageWriter()
    writer.SetInputData(image)
    writer.SetFileName(image_path)
    writer.Update()


def read_vtk_poly_data(surface_path):

    surf_reader = vtk.vtkPolyDataReader()
    surf_reader.SetFileName(surface_path)
    surf_reader.Update()

    return surf_reader.GetOutput()

def write_vtk_poly_data(poly_data, path):

    surf_writer = vtk.vtkPolyDataWriter()
    surf_writer.SetInputData(poly_data)
    surf_writer.SetFileName(path)
    surf_writer.Update()


def load_images(image_path):

    sitk_vol = sitk.ReadImage(image_path)
    vtk_vol = read_vtk_nifti_image(image_path)

    return sitk_vol, vtk_vol