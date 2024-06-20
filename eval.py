import nibabel as nib
import numpy as np
import os

#directories in which I saved the nifti files (mask 1 is the ground truth file)
mask1_path = r'C:\Users\mijan\Desktop\Summer Research\rsna-cspine-segmentations\segmentations\1.2.826.0.1.3680043.780.nii'
mask2_path = r'C:\Users\mijan\Desktop\Summer Research\rsna-cspine-segmentations\nifti_source_files_segmentations\1.2.826.0.1.3680043.780\segmentations\vertebrae_C1.nii.gz'

mask1_img = nib.load(mask1_path)
mask2_img = nib.load(mask2_path)

mask1_data = mask1_img.get_fdata()
mask2_data = mask2_img.get_fdata()

#checking shape of the two masks to make sure they are the same
print(f"Shape of mask1: {mask1_data.shape}")
print(f"Shape of mask2: {mask2_data.shape}")

mask1_data = (mask1_data > 0).astype(int)
mask2_data = (mask2_data > 0).astype(int)

intersection_data = np.logical_and(mask1_data, mask2_data).astype(int)

intersect_num = np.sum(intersection_data)

#to make sure there is something there...
print(mask1_data.max())
print(mask1_data.sum())
print(mask2_data.max())
print(mask2_data.sum())

#hopefully a number that makes sense
print(f"Intersection number = {intersect_num}")
