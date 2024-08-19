#This program is used to view patient files slice by slice when saved in npz format
#For input it only requires the path to the npz file and, depending on how the file was saved/what you want to view in it, a key

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# Path to the .npz file to inspect
npz_file_path = r""

# Load the .npz file
npz_file = np.load(npz_file_path)

#key depends on how the npz file is saved
key = 'imgs'

#Starting slice index (set to higher initial value if there are problems seeing results. It seemed to help me at times)
slice_index = 0

print(f"Shape of the npz data: {npz_file[key].shape}")
print(f"Data type of the npz data: {npz_file[key].dtype}")
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)

img = ax.imshow(npz_file[key][slice_index], cmap='gray')
ax.set_title(f"Slice {slice_index}")
ax.axis('off')

def update(val):
    slice_index = int(slice_slider.val)
    img.set_data(npz_file[key][slice_index])
    ax.set_title(f"Slice {slice_index}")
    fig.canvas.draw_idle()

ax_slice = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slice_slider = Slider(ax_slice, 'Slice', 0, npz_file[key].shape[0] - 1, valinit=slice_index, valstep=1)

slice_slider.on_changed(update)
plt.show()
