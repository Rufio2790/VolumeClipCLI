import unittest
import os
from tests import data_path
from simple_clip import load_and_process

class TestSimpleClip(unittest.TestCase):

    def setUp(self):
        self.image_path = os.path.join(data_path, 'scene', 'ref.nii.gz')
        self.surf_path = os.path.join(data_path, 'scene', 'models', 'lh_pial.vtk')
        self.surf_not_centered_path = os.path.join(data_path, 'scene', 'models', 'lh_pial_no_centered.vtk')
        self.transform_path = os.path.join(data_path, 'auxiliary', 'centered2ref.tfm')

    def test_clipping(self):
        load_and_process(self.image_path, self.surf_path, os.path.join(data_path, 'test_result.mha'),
                         inside_bool=True)

    def test_clipping_applying_matrix(self):
        load_and_process(self.image_path, self.surf_not_centered_path, os.path.join(data_path, 'test_result.mha'),
                         inside_bool=True, transform_path=self.transform_path)

    def test_nifti_output(self):
        load_and_process(self.image_path, self.surf_path, os.path.join(data_path, 'test_result.nii.gz'),
                         inside_bool=True)

if __name__ == '__main__':
    unittest.main()
