#Extracts bounding box coordinates to be given as input to MedSAM box prompt during segmentation

import nibabel as nib
import numpy as np
import os
import fnmatch
import csv

def search_files(directory, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches

#dir = path to ground truth files
dir = r""
GT_files = search_files(dir, '*.nii')

for i in GT_files:
    print(i)

with open('bb_info.csv', 'w', newline='') as csvfile:
    fieldnames = ['Patient id #', 'min_x', 'min_y', 'max_x', 'max_y', 'z']
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(fieldnames)

def write_info(data):
    with open('bb_info.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)


patient_bb_info = [0, 0, 0, 0, 0, 0]

for gt in GT_files:

    img = nib.load(gt)
    img_data = img.get_fdata()

    length = img_data.shape[2]
    
    if gt[103].isdigit():
        patient_bb_info[0] = gt[99:104:1]
    elif gt[102].isdigit():
        patient_bb_info[0] = gt[99:103:1]
    else:
        patient_bb_info[0] = gt[99:102:1]

    for i in range(length):
        slice_data = img_data[:, :, i]

        mask_indices = np.argwhere(slice_data > 0)
    
        if mask_indices.size == 0:
            patient_bb_info[1] = 0
            patient_bb_info[2] = 0
            patient_bb_info[3] = 0
            patient_bb_info[4] = 0
            patient_bb_info[5] = i
            write_info(patient_bb_info)
        else:
            # Get min and max x and y coordinates to form the bounding box
            min_coords = mask_indices.min(axis=0)
            max_coords = mask_indices.max(axis=0)
            min_x, min_y = min_coords
            max_x, max_y = max_coords

            patient_bb_info[1] = min_x
            patient_bb_info[2] = min_y
            patient_bb_info[3] = max_x
            patient_bb_info[4] = max_y
            patient_bb_info[5] = i

            write_info(patient_bb_info)

print("Done")
