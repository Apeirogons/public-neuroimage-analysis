# The first step of the DTI pipeline, using fsl commands. Generates coregistered FA, L1, MD, and RD.
import os

# Script needs to be in same folder as images and called from there.
IMAGE_FOLDER = "for_matthew" # Folder containing image files. 
ATLAS_PARENT = "atlases/JHU-ICBM-FA-1mm.nii.gz" # Folder containing JHU atlases.

def eddy_current(identifier, regenerate=False):
    """
    Executes eddy_correct, which corrects for eddy currents. Takes a long time.
    Args:
        identifier (str): unique image number
        regenerate (bool): whether or not to redo the command even though one of its outputs already exists
    """
    location = IMAGE_FOLDER +'/hc_'+identifier
    files_in_loc = os.listdir(location)
    for f in files_in_loc:
        if f.find('nii') != -1 and f.find('str') == -1:
            target = location+'/'+f
            break
    if (not os.path.exists(location + "/SlicerDataCorrected.nii.gz")) or regenerate:
        command = "eddy_correct %s %s/SlicerDataCorrected.nii.gz 0" % (target, location)
        return os.system(command)
    else:
        print(location + "/SlicerDataCorrected.nii.gz already exists.")
        return 0

def BET(identifier, regenerate=False):
    """
    Executes BET, which isolates the brain. 
    Args:
        identifier (str): unique image number
        regenerate (bool): whether or not to redo the command even though one of its outputs already exists
    """
    location = IMAGE_FOLDER +'/hc_'+identifier
    if (not os.path.exists(location + "/SlicerDataCorrected_brain.nii.gz")) or regenerate:
        command = "/usr/local/fsl/bin/bet %s/SlicerDataCorrected %s/SlicerDataCorrected_brain -f 0.05 -g 0 -m" % (location, location)
        return os.system(command)
    else:
        print(location + "/SlicerDataCorrected_brain.nii.gz already exists.")
        return 0 

def DTIFIT(identifier, regenerate=False):
    """
    Executes DTIFIT, which estimates the DTI image.
    Args:
        identifier (str): unique image number
        regenerate (bool): whether or not to redo the command even though one of its outputs already exists
    """
    location = IMAGE_FOLDER +'/hc_'+identifier
    bvec = ''
    bval = ''
    files_in_loc = os.listdir(location)
    for f in files_in_loc:
        if f.find('bvec') != -1:
            bvec = location+'/'+f
        elif f.find('bval') != -1:
            bval = location+'/'+f
        if bvec != '' and bval != '':
            break
    if (not os.path.exists(location + "/dti_FA.nii.gz")) or regenerate:
        command = "/usr/local/fsl/bin/dtifit --data=%s/SlicerDataCorrected.nii.gz --out=%s/dti --mask=%s/SlicerDataCorrected_brain_mask.nii.gz --bvecs=%s --bvals=%s" % (location, location, location, bvec, bval)
        return os.system(command)
    else:
        print(location + "/dti_FA.nii.gz already exists.")
        return 0 

def registration(identifier, target, regenerate=False):
    """
    Executes flirt, which registers the image based on the FA to the JHU atlas.
    Args:
        identifier (str): unique image number
        target (str): path to JHU 1mm FA atlas
        regenerate (bool): whether or not to redo the command even though one of its outputs already exists
    """
    location = IMAGE_FOLDER +'/hc_'+identifier
    if (not os.path.exists(location + "/dti_FA_coreg.mat")) or regenerate:
        command = "/usr/local/fsl/bin/flirt -in %s/dti_FA.nii.gz -ref %s -out %s/dti_FA_coreg.nii.gz -omat %s/dti_FA_coreg.mat -bins 256 -cost corratio -searchrx -120 120 -searchry -120 120 -searchrz -120 120 -dof 12  -interp trilinear" % (location,target, location, location)
        return os.system(command)
    else:
        print(location + "/dti_FA_coreg.mat already exists.")
        return 0 

def compute_RD(identifier, regenerate=False):
    """
    Takes the mean of L2 and L3, which results in RD.
    Args:
        identifier (str): unique image number
        regenerate (bool): whether or not to redo the command even though one of its outputs already exists
    """
    location = IMAGE_FOLDER +'/hc_'+identifier
    if (not os.path.exists(location + "/dti_RD.nii.gz")) or regenerate:
        command = '/usr/local/fsl/bin/fslmaths %s/dti_L2.nii.gz -add %s/dti_L3.nii.gz -div 2 %s/dti_RD.nii.gz' % (location, location, location)
        return os.system(command)
    else:
        print(location + "/dti_RD.nii.gz already exists.")
        return 0 

def other_registrations(identifier, target, regenerate=False):
    """
    Registers the other brain metrics based on the FA registration to the JHU atlas.
    Args:
        identifier (str): unique image number
        target (str): path to JHU 1mm FA atlas
        regenerate (bool): whether or not to redo the command even though one of its outputs already exists
    """
    location = IMAGE_FOLDER +'/hc_'+identifier
    if (not os.path.exists(location + "/dti_MD_coreg.nii.gz")) or regenerate:
        for metric in ['L1', 'MD', 'RD']:
            command = "/usr/local/fsl/bin/flirt -in %s/dti_%s.nii.gz -ref %s -out %s/dti_%s_coreg.nii.gz -applyxfm -init %s/dti_FA_coreg.mat -interp trilinear" % (location, metric, target, location, metric, location)
            os.system(command)
        return 0 
    else:
        print(location + "/dti_MD_coreg.mat already exists.")
        return 0 

# Step 0: Get all of the folders.
current_dir = os.listdir(IMAGE_FOLDER)
image_folders = []

for d in current_dir:
    if d.find('.') == -1:
        image_folders.append(d)
print ("Folders: " + str(image_folders)) 

for folder in image_folders[:-1]: #I don't feel like processing the last one.
    identifier = folder[-4:]
    print("Starting "+ identifier)
    
    # Step 1: Use eddy_current to fix image distortions.
    print(eddy_current(identifier, regenerate=False))

    # Step 2: Use BET brain extraction to extract the brain
    print(BET(identifier, regenerate=False))

    # Step 3: Reconstruct diffusion tensors.
    print(DTIFIT(identifier, regenerate=False))

    # Step 4: Register the image to JHU atlas.
    print(registration(identifier, ATLAS_PARENT, regenerate=False))

    # Step 5: Obtain the RD by taking the mean of L2 and L3. 
    print(compute_RD(identifier, regenerate=False))

    # Step 6: Register other images of interest to FA. 
    print(other_registrations(identifier,ATLAS_PARENT, regenerate=False))
 