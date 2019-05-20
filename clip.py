import vtk
import numpy as np
import SimpleITK as sitk


def clip_volume_with_model(surface, volume, out=False):
    """
    Given a surface, it clips the volume providing the inside or outside part of the volume.
    The surface must be closed.
    :param surface:
    :param volume:
    :param out: if True, provide the external part of the volume (default is False)

    :return:
    """

# Determine the transform between the box and the image IJK coordinate systems

rasToModel = vtk.vtkMatrix4x4()
if clippingModel.GetTransformNodeID() != None:
    modelTransformNode = slicer.mrmlScene.GetNodeByID(clippingModel.GetTransformNodeID())
    boxToRas = vtk.vtkMatrix4x4()
    modelTransformNode.GetMatrixTransformToWorld(boxToRas)
    rasToModel.DeepCopy(boxToRas)
    rasToModel.Invert()

ijkToRas = vtk.vtkMatrix4x4()
inputVolume.GetIJKToRASMatrix(ijkToRas)

ijkToModel = vtk.vtkMatrix4x4()
vtk.vtkMatrix4x4.Multiply4x4(rasToModel, ijkToRas, ijkToModel)
modelToIjkTransform = vtk.vtkTransform()
modelToIjkTransform.SetMatrix(ijkToModel)
modelToIjkTransform.Inverse()

transformModelToIjk = vtk.vtkTransformPolyDataFilter()
transformModelToIjk.SetTransform(modelToIjkTransform)
transformModelToIjk.SetInputConnection(clippingModel.GetPolyDataConnection())

# Use the stencil to fill the volume

# Convert model to stencil
polyToStencil = vtk.vtkPolyDataToImageStencil()
polyToStencil.SetInputConnection(transformModelToIjk.GetOutputPort())
polyToStencil.SetOutputSpacing(inputVolume.GetImageData().GetSpacing())
polyToStencil.SetOutputOrigin(inputVolume.GetImageData().GetOrigin())
polyToStencil.SetOutputWholeExtent(inputVolume.GetImageData().GetExtent())

# Apply the stencil to the volume
stencilToImage = vtk.vtkImageStencil()
stencilToImage.SetInputConnection(inputVolume.GetImageDataConnection())
stencilToImage.SetStencilConnection(polyToStencil.GetOutputPort())
if clipOutsideSurface:
    stencilToImage.ReverseStencilOff()
else:
    stencilToImage.ReverseStencilOn()
stencilToImage.SetBackgroundValue(fillValue)
stencilToImage.Update()

# Update the volume with the stencil operation result
outputImageData = vtk.vtkImageData()
outputImageData.DeepCopy(stencilToImage.GetOutput())

outputVolume.SetAndObserveImageData(outputImageData);
outputVolume.SetIJKToRASMatrix(ijkToRas)

# Add a default display node to output volume node if it does not exist yet
if not outputVolume.GetDisplayNode:
    displayNode = slicer.vtkMRMLScalarVolumeDisplayNode()
    displayNode.SetAndObserveColorNodeID("vtkMRMLColorTableNodeGrey")
    slicer.mrmlScene.AddNode(displayNode)
    outputVolume.SetAndObserveDisplayNodeID(displayNode.GetID())

return True