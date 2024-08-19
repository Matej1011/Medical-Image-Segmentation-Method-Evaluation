import dicom2nifti
import os

dicom_directory = r'C:\Users\mijan\Desktop\Summer Research\test_images\1.2.826.0.1.3680043.22327'
nifti_output_path = r'C:\Users\mijan\Desktop\Summer Research\test_images\output'

dicom2nifti.convert_directory(dicom_directory, nifti_output_path, reorient=True)
print(f"Conversion complete. NIfTI file saved.")
