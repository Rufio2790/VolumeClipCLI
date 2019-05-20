import numpy as np
import vtk

def get_sitkImg_transform(image):

    translation = np.asarray(image.GetOrigin()).reshape(3, 1)
    rotation = np.asarray(image.GetDirection()).reshape(3, 3)

    transform_from_sitk = np.c_[rotation, translation]
    transform_from_sitk = np.vstack([transform_from_sitk, [0, 0, 0, 1]])

    return transform_from_sitk


def get_ras2ijk(image, lps=False):

    LPStoRAS = np.matrix([[-1, 0, 0, 0],
                          [0, -1, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])

    LPSorientation = get_sitkImg_transform(image)

    spacing = np.asarray(image.GetSpacing())
    spacing_matrix = np.eye(4)
    for i in range(3):
        spacing_matrix[i][i] = spacing[i]

    transform_from_sitk = np.dot(LPSorientation, spacing_matrix)
    if not lps:
        transform_from_sitk_ras = np.dot(LPStoRAS, transform_from_sitk)

        return np.linalg.inv(transform_from_sitk_ras)
    return np.linalg.inv(transform_from_sitk)


def transform_poly_data(poly_data, transform):
    """
    Transform all points of polydata structure given a numpy matrix transform.
    Internally it converts the matrix and apply to the poly data using vtkTransformPolyDataFilter.

    :param poly_data:
    :param transform:
    :return: transformed poly_data
    """
    vtk_matrix = vtk.vtkMatrix4x4()
    vtk_matrix.DeepCopy(np.asarray(transform).ravel())
    vtk_transform = vtk.vtkTransform()
    vtk_transform.SetMatrix(vtk_matrix)

    poly_data_transform = vtk.vtkTransformPolyDataFilter()
    poly_data_transform.SetTransform(vtk_transform)
    poly_data_transform.SetInputData(poly_data)
    poly_data_transform.Update()

    return poly_data_transform.GetOutput()