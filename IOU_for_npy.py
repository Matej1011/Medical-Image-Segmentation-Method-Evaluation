#This program was used temporarily to test the evaluation of .npy files
#Originally, MedSAM's preprocessing program output .npy files and this code was used before editing the preprocessing code to output .npz files

import nibabel as nib
import numpy as np
import os
import fnmatch
import csv
import cv2

def search_files(directory, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches

#dir = path to npy files
dir = r""
MedSAM_masks = search_files(dir, '*.npy')

dir = r'C:\Users\mijan\Desktop\Summer Research\rsna-cspine-segmentations'
GT_files = search_files(dir, '*.nii')

total_iou = 0
segment_IOU = 0

#writing a new csv file in which I'll add the IOU data for the patients
with open('MedSAM_IOU_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['Patient id #', 'Slice #','IOU']
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(fieldnames)

def write_info(data):
    with open('MedSAM_IOU_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def calculate_IOU(ground_truth_data, mask_directory, i):

    # Load the numpy file for the mask
    mask_img = np.load(mask_directory)

    mask_img = cv2.rotate(mask_img, cv2.ROTATE_90_CLOCKWISE)

    ground_truth_data = ground_truth_data[:, :, i]
    mask_img = (mask_img > 0).astype(int)

    # Calculate the intersection of the masks
    intersection_data = np.logical_and(ground_truth_data, mask_img)
    union_data = np.logical_or(ground_truth_data, mask_img)

    intersect_num = np.sum(intersection_data)
    union_num = np.sum(union_data)

    assert union_num != 0, "Union_num is zero for patient ID"

    iou_num = intersect_num / union_num

    return iou_num

def set_slice_num(mask_idx, i):
    if i > 9:
        if MedSAM_masks[mask_idx][75].isdigit():
            return int(MedSAM_masks[mask_idx][74:76:1])
        else:
            return int(MedSAM_masks[mask_idx][74])
    else:
        return int(MedSAM_masks[mask_idx][74])

mask_index = 0
iou = 0
slice_num = 0

#list to hold slice # and IOU
patient_data = ['', 0, 0]

gt = r"C:\Users\mijan\Desktop\Summer Research\rsna-cspine-segmentations\segmentations\1.2.826.0.1.3680043.10633.nii"

for i in range(30):

    set_slice_num(mask_index, i)

    ground_truth_img = nib.load(gt)
    ground_truth_data = ground_truth_img.get_fdata()

    if gt[103].isdigit():
        patient_data[0] = gt[99:104:1]
    elif gt[102].isdigit():
        patient_data[0] = gt[99:103:1]
    else:
        patient_data[0] = gt[99:102:1]

    #used to make sure the correct mask is being compared with the correct slice because the array is not organized correctly
    while slice_num != i:
        mask_index += 1
        slice_num = set_slice_num(mask_index, i)

    print("Comparing", gt[99:104:1], "and S", slice_num)
    segment_IOU = calculate_IOU(ground_truth_data, MedSAM_masks[mask_index], i)
    total_iou += segment_IOU
    patient_data[2] = segment_IOU

    write_info(patient_data)

    mask_index = 0
    iou = 0

print("Average of all IOUs: ", (total_iou / 40))
