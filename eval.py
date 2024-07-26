#I've removed comments that I had before which were just code I used to troubleshoot/debug
#It was mainly print statements that told me things like data shape, max/min values, and patient numbers

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

# Below are the root directories containing the masks from total segmentator and ground truth files
# I've checked the contents of these and made sure they have the correct files and they correctly gather and organize them
dir = r'C:\Users\mijan\Desktop\Summer Research\rsna-cspine-segmentations\nifti_source_files_segmentations'
TS_masks = search_files(dir, '*nii.gz')

dir = r'C:\Users\mijan\Desktop\Summer Research\rsna-cspine-segmentations'
GT_files = search_files(dir, '*.nii')

total_iou = 0
segment_IOU = 0

def calculate_IOU(ground_truth_data, mask_directory, i):

    # Load the NIfTI file for the mask
    mask_img = nib.load(mask_directory)
    mask_data = mask_img.get_fdata()


    ground_truth_data = (ground_truth_data == i).astype(int)
    mask_data = (mask_data > 0).astype(int)

    # Calculate the intersection of the masks
    intersection_data = np.logical_and(ground_truth_data, mask_data)
    union_data = np.logical_or(ground_truth_data, mask_data)


    intersect_num = np.sum(intersection_data)
    union_num = np.sum(union_data)

    assert union_num != 0, "Union_num is zero for patient ID"

    iou_num = intersect_num / union_num


    return iou_num

mask_index = 1 #used to move through TS_masks and compare the correct generated masks with ground truth files
patient_num = 0 #This is just so that I can print something out every iteration and I know the code is running properly
iou = 0

#list to hold the averages of each segment's IOU
segment_averages = [0, 0, 0, 0, 0, 0, 0, 0]

for gt in GT_files:

    ground_truth_img = nib.load(gt)
    ground_truth_data = ground_truth_img.get_fdata()

    #after loading one of the ground truth files, compare it with masks for C1 to T1 (8 total) and track value for overall IOU and for each segment
    for i in range(8):
        segment_IOU = calculate_IOU(ground_truth_data, TS_masks[mask_index], i+1)
        total_iou += segment_IOU
        segment_averages[i] += segment_IOU
        mask_index += 1

    mask_index += 1
    patient_num += 1
    iou = 0
    print("Files processed: ", patient_num)

# The rest below is just printing out results
print("Average of all IOUs: ", (total_iou / 87 / 8))

for i in range(8):
    if i < 7:
        print("IOU average for C", i+1, ": ", segment_averages[i] / 87)
    else:
        print("IOU average for T1: ", segment_averages[7] / 87)
