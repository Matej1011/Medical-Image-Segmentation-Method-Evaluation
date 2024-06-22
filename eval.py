
import nibabel as nib
import numpy as np
import os
import fnmatch

def search_files(directory, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches

dir = r'C:\Users\mijan\Desktop\Summer Research\rsna-cspine-segmentations\nifti_source_files_segmentations'
compressed_niftis = search_files(dir, '*nii.gz')

dir = r'C:\Users\mijan\Desktop\Summer Research\rsna-cspine-segmentations'
files = search_files(dir, '*.nii')

sum = 0
total_iou = 0

#this loops through the masks/segmentations from totalSegmentator
for segmentations in compressed_niftis:
    sum = sum+1
print('Segmentations: ')
print(sum)

sum = 0
#this loops through the ground truths
for niftis in files:
    sum=sum+1
print('Ground truths: ')
print(sum)

def calculate_IOU(ground_truth_directory, mask_directory, segmentation_num):

    # Load the NIfTI files
    #mask 1 is ground truth
    
    ground_truth_img = nib.load(ground_truth_directory)
    mask_img = nib.load(mask_directory)

    # Get the data from the NIfTI images
    ground_truth_data = ground_truth_img.get_fdata()
    mask_data = mask_img.get_fdata()

    #print(f"Shape of mask1: {ground_truth_data.shape}")
    #print(f"Shape of mask2: {mask_data.shape}")

    # Ensure the masks are binary (values 0 or 1)
    ground_truth_data = (ground_truth_data > 0).astype(int)
    mask_data = (mask_data > 0).astype(int)

    # Calculate the intersection of the masks
    intersection_data = np.logical_and(ground_truth_data, mask_data).astype(int)
    union_data = np.logical_or(ground_truth_data, mask_data).astype(int)

    intersect_num = np.sum(intersection_data)
    union_num = np.sum(union_data)
    if union_num != 0:
        iou_num = intersect_num / union_num * 100
    else:
        iou_num = 0
    
    #print(mask1_data.max())
    #print(mask1_data.sum())
    #print(mask2_data.max())
    #print(mask2_data.sum())

    #print(f"Intersection number = {intersect_num}")
    #print(f"Union number = {union_num}")
    #print(f"IOU (%): {iou_num}")
    
    print("Mask #: ", seg_num)

    return iou_num


#iterate through the list of segmentations and add to the total IOU score (which will probably have to be changed)
GT_index = -1
mask_index = 0
seg_num = 1
patient_num = 1

for gt in files:
    GT_index += 1
    mask_index +=1
    print("IOU: ", total_iou)
    print("Patient #: ", patient_num)
    patient_num += 1
    for i in range(8):
        total_iou += calculate_IOU(files[GT_index], compressed_niftis[mask_index], seg_num)
        mask_index +=1
        seg_num += 1
