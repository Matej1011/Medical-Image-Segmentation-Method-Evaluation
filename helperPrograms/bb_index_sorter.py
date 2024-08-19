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

dir = r'C:\Users\mijan\Desktop\Summer Research\rsna-cspine-segmentations'
GT_files = search_files(dir, '*.nii')

def read_bb_data(row, data):
    line = 0
    with open('bb_info.csv', mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for r in reader:
            if line != row:
                line+=1
            else:
                return r[data]

with open('bb_index_info.csv', 'w', newline='') as csvfile:
    fieldnames = ['Patient id #', 'csv_index']
    writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(fieldnames)

def write_info(data):
    with open('bb_index_info.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

patient_info = ['', '']
csv_index = 0

for gt in GT_files:
    if gt[103].isdigit():
        patient_info[0] = gt[99:104:1]
    elif gt[102].isdigit():
        patient_info[0] = gt[99:103:1]
    else:
        patient_info[0] = gt[99:102:1]
    while read_bb_data(csv_index, "Patient id #") != patient_info[0]:
        csv_index += 1
    patient_info[1] = csv_index

    write_info(patient_info)
print("Done")