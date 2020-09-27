# Extracts relevant brain volumes and generates images using Slicer. The second step of the DTI pipeline.
# Because running Slicer from command-line doesn't work on my machine, this must be copy-pasted into the Slicer GUI.
# Also, the GUI handles whitespace weirdly. 

import slicer
import os
from LabelStatistics import LabelStatisticsLogic
import ScreenCapture
from time import sleep

target_folder = '../for_matthew'# Path to folder containing images.
target_files = ['dti_FA_coreg.nii.gz', 'dti_L1_coreg.nii.gz', 'dti_MD_coreg.nii.gz', 'dti_RD_coreg.nii.gz']# Coregistered images of interest (processed by automate_fsl.py)

flag, atlas = slicer.util.loadVolume('../atlases/JHU-ICBM-labels-1mm.nii.gz', properties={'show':1,'labelmap':1}, returnNode=True)# Load JHU atlas labels

if not os.path.exists('../slicer_outputs'): os.mkdir('../slicer_outputs')# Create slicer output folders


if not os.path.exists('../slicer_imgs'): os.mkdir('../slicer_imgs')


current_dir = os.listdir(target_folder) 
image_folders = []

for d in current_dir:
    if d.find('.') == -1:
        image_folders.append(d)

        
print ("Folders: " + str(image_folders)) 

for folder in image_folders:
    for i, f in enumerate(target_files):
        loc = '%s/%s/%s' % (target_folder, folder, f)
        if os.path.exists(loc):
            name = f.split('.')[0]
            flag, vol = slicer.util.loadVolume(loc, properties={'show':1}, returnNode=True)# Load image metric
            stats = LabelStatisticsLogic(vol, atlas)
            stats.saveStats('../slicer_outputs/%s_%s.csv' % (folder, str(name)))# Compute and save metrics to csv
            cap = ScreenCapture.ScreenCaptureLogic()
            cap.captureImageFromView(None,'../slicer_imgs/%s_%s.png' % (folder, str(name)))# Save image for error-checking
            slicer.mrmlScene.RemoveNode(vol)# Remove volume to allow visualization of next volume



