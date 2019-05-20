import vtk


def clip_volume_with_surface_model(polydata, vtk_image, clip_outside_surface=False, fill_value=0):
    """
    Given a surface, it clips the volume providing the inside or outside part of the volume.
    It must be a closed mesh, and should be correctly mapped with the vtkVolume.

    :param polydata:
    :param vtk_image:
    :param clip_outside_surface: if True, provide the external part of the volume (default is False)

    :return: clipped_vtk_image
    """
    # Convert model to stencil
    polyToStencil = vtk.vtkPolyDataToImageStencil()
    polyToStencil.SetInputData(polydata)
    polyToStencil.SetOutputSpacing(vtk_image.GetSpacing())
    polyToStencil.SetOutputOrigin(vtk_image.GetOrigin())
    polyToStencil.SetOutputWholeExtent(vtk_image.GetExtent())
    polyToStencil.Update()
    # Apply the stencil to the volume
    stencilToImage = vtk.vtkImageStencil()
    stencilToImage.SetInputData(vtk_image)
    stencilToImage.SetStencilData(polyToStencil.GetOutput())
    if clip_outside_surface:
        stencilToImage.ReverseStencilOff()
    else:
        stencilToImage.ReverseStencilOn()
    stencilToImage.SetBackgroundValue(fill_value)
    stencilToImage.Update()

    # Update the volume with the stencil operation result
    outputImageData = vtk.vtkImageData()
    outputImageData.DeepCopy(stencilToImage.GetOutput())

    return outputImageData
