"""
--i=data/scene/ref.nii.gz --s=data/scene/models/lh_pial.vtk --in=True, --o=data/trial.mha
"""

import os
import sys
import logging
import SimpleITK as sitk
import argparse
import numpy as np

import lib.clip as clip
import lib.read_and_write as rw
import lib.transforms as trsf

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

ras2lps = np.identity(4)
ras2lps[0, 0] = -1
ras2lps[1, 1] = -1

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--image', type=str, help='Image path containing the image to be clipped',
                        required=True)
    parser.add_argument('-s', '--surf', type=str, help='Surface path model', required=True)
    parser.add_argument('--inside', type=bool, help='True: Keep volume INSIDE (True) or OUTSIDE (False) the model; '
                                               'default is True ', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output path', required=True)
    parser.add_argument('-t', '--transform', type=str, help='Transform to apply to the surfaces before clipping '
                                                            '(optional')

    logging.info("Parsing arguments...")
    args = parser.parse_args()
    load_and_process(args.image, args.surf, args.output, inside_bool=args.inside, transform_path=args.transform)



def load_and_process(image_path, surface_path, output_path, inside_bool=False, transform_path=None):
    logging.info("Reading images and surfaces...")
    # loading images as itk and vtk volume
    sitk_im, vtk_im = rw.load_images(image_path)
    # forcing spacing to 1 for vtk image
    vtk_im.SetSpacing([1., 1., 1.])

    # loading surface
    surf = rw.read_vtk_poly_data(surface_path)

    if transform_path:
        t = sitk.ReadTransform(transform_path)
        t = np.array(t.GetParameters())
        c2r = np.identity(4)
        c2r[:3, :3] = t[:9].reshape(3, 3)
        c2r[:3, 3] = t[9:]
        print('Reading centered2ref')
        print(c2r)
        c2r = np.dot(np.linalg.inv(c2r), ras2lps)
        c2r = np.dot(ras2lps, c2r)
        print('Transforming to RAS')
        print(c2r)
        surf = trsf.transform_poly_data(surf, c2r)

        rw.write_vtk_poly_data(surf, os.path.join(os.path.dirname(output_path), "trsf_surf.vtk"))

    # getting image transformation matrix
    ras2ijk = trsf.get_ras2ijk(sitk_im)

    # transforming the surface to match with image at IJK -> Getting from RAS because surfaces are in RAS
    surf_at_ijk = trsf.transform_poly_data(surf, ras2ijk)

    logging.info("Clipping the image...")
    # clipping the image
    out_vtk_image = clip.clip_volume_with_surface_model(surf_at_ijk, vtk_im, clip_outside_surface=inside_bool)

    # writing temporary nifty image without spatial information
    temp_file_path = os.path.join(os.path.dirname(output_path), "temp.nii.gz")
    rw.write_vtk_nifti_image(out_vtk_image, temp_file_path)

    # reading the same image with itk
    out_image = sitk.ReadImage(temp_file_path)
    # applying correct spatial informations (LPS system)
    image_lps = trsf.get_sitkImg_transform(sitk_im)
    out_image.SetSpacing(sitk_im.GetSpacing())
    out_image.SetDirection(image_lps[:3, :3].ravel())
    out_image.SetOrigin(image_lps[:3, 3])

    logging.info("Saving image...")
    # writing the clipped image
    sitk.WriteImage(out_image, output_path)

    # removing temporary image
    os.remove(temp_file_path)

if __name__ == "__main__":

    main()



