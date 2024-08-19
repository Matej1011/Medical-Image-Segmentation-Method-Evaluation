import nibabel as nib
import numpy as np
import os
import fnmatch
import csv
import cv2
from scipy.ndimage import zoom
from time import process_time

def search_files(directory, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches

dir = r"C:\Users\mijan\Desktop\Summer Research\MedSAM_generated_masks"
MedSAM_masks = search_files(dir, '*.npz')

dir = r'C:\Users\mijan\Desktop\Summer Research\rsna-cspine-segmentations'
GT_files = search_files(dir, '*.nii')

total_iou = 0
slice_IOU = 0

#writing a new csv file in which I'll add the IOU data for the patients
#with open('MedSAM_IOU_data.csv', 'w', newline='') as csvfile:
#    fieldnames = ['Patient id #', 'IOU']
#    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    writer.writerow(fieldnames)

def write_info(data):
    with open('MedSAM_IOU_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def calculate_IOU(ground_truth_data, mask, i):

    mask = cv2.rotate(mask, cv2.ROTATE_90_CLOCKWISE)

    ground_truth_data = ground_truth_data[:, :, i]
    mask_img = (mask > 0).astype(int)

    # Calculate the intersection of the masks
    intersection_data = np.logical_and(ground_truth_data, mask_img)
    union_data = np.logical_or(ground_truth_data, mask_img)

    intersect_num = np.sum(intersection_data)
    union_num = np.sum(union_data)

    #assert union_num != 0, "Union_num is zero for patient ID"
    if union_num == 0:
        return 0.0

    iou_num = intersect_num / union_num

    print("Slice #:", i, " IOU_num: ", iou_num)

    return iou_num

mask_index = 0
iou = 0
slice_num = 0
length = 0

#list to hold each patient's IOU
patient_data = ['', 0]

gt = r"C:\Users\mijan\Desktop\Summer Research\rsna-cspine-segmentations\segmentations\1.2.826.0.1.3680043.14267.nii"

for x in GT_files:

    ground_truth_img = nib.load(gt)
    ground_truth_data = ground_truth_img.get_fdata()

    if gt[103].isdigit():
        patient_data[0] = gt[99:104:1]
        length = 5
    elif gt[102].isdigit():
        patient_data[0] = gt[99:103:1]
        length = 4
    else:
        patient_data[0] = gt[99:102:1]
        length = 3

    length = 5
    patient_data[0] = '14267'

    while (patient_data[0]) != MedSAM_masks[mask_index][62:(62+length):1]:
        mask_index += 1

    #after loading one of the ground truth files, compare it with masks for C1 to T1 (8 total) and track value for overall IOU and for each segment
    #also update value for each segment of specific patient
    mask_npz = np.load(MedSAM_masks[mask_index])
    slices = mask_npz['masks'].shape[0]

    for i in range(slices):
        mask = mask_npz['masks'][i]
        mask = zoom(mask, 0.5)
        patient_data[1] += calculate_IOU(ground_truth_data, mask, i)
    
    patient_data[1] /= slices
    total_iou += patient_data[1]

    write_info(patient_data)

    mask_index = 0
    iou = 0
    break

print("Average of all IOUs: ", (total_iou))
