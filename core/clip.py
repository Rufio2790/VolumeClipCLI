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
    poly_to_stencil = vtk.vtkPolyDataToImageStencil()
    poly_to_stencil.SetInputData(polydata)
    poly_to_stencil.SetOutputSpacing(vtk_image.GetSpacing())
    poly_to_stencil.SetOutputOrigin(vtk_image.GetOrigin())
    poly_to_stencil.SetOutputWholeExtent(vtk_image.GetExtent())
    poly_to_stencil.Update()
    # Apply the stencil to the volume
    stencil_to_image = vtk.vtkImageStencil()
    stencil_to_image.SetInputData(vtk_image)
    stencil_to_image.SetStencilData(poly_to_stencil.GetOutput())
    if clip_outside_surface:
        stencil_to_image.ReverseStencilOff()
    else:
        stencil_to_image.ReverseStencilOn()
    stencil_to_image.SetBackgroundValue(fill_value)
    stencil_to_image.Update()

    # Update the volume with the stencil operation result
    output_image_data = vtk.vtkImageData()
    output_image_data.DeepCopy(stencil_to_image.GetOutput())

    return output_image_data
