"""
--i=data/scene/ref.nii.gz --s=data/scene/models/lh_pial.vtk --in=True, --o=data/trial.mha
"""

import os
import sys
import logging
import SimpleITK as sitk
import argparse
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

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--image', type=str, help='Image path containing the image to be clipped',
                        required=True)
    parser.add_argument('-s', '--surf', type=str, help='Surface path model', required=True)
    parser.add_argument('--inside', type=bool, help='True: Keep volume INSIDE (True) or OUTSIDE (False) the model; '
                                               'default is True ', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output path', required=True)

    logging.info("Parsing arguments...")
    args = parser.parse_args()

    logging.info("Reading images and surfaces...")
    # loading images as itk and vtk volume
    sitk_im, vtk_im = rw.load_images(args.image)
    # forcing spacing to 1 for vtk image
    vtk_im.SetSpacing([1., 1., 1.])

    # loading surface
    surf = rw.read_vtk_poly_data(args.surf)

    # getting image transformation matrix
    ras2ijk = trsf.get_ras2ijk(sitk_im)

    # transforming the surface to match with image at IJK -> Getting from RAS because surfaces are in RAS
    surf_at_ijk = trsf.transform_poly_data(surf, ras2ijk)

    logging.info("Performing Clipping...")
    # clipping the image
    out_vtk_image = clip.clip_volume_with_surface_model(surf_at_ijk, vtk_im, clip_outside_surface=args.inside)

    # writing temporary nifty image without spatial information
    temp_file_path = os.path.join(os.path.dirname(args.output), "temp.nii.gz")
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
    sitk.WriteImage(out_image, args.output)

    # removing temporary image
    os.remove(temp_file_path)

if __name__ == "__main__":

    main()



