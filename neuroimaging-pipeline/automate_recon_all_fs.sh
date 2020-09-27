#!/bin/bash

# The first step of the structural pipeline, using recon-all to generate a lot of raw extracted metrics.

# Loading freesurfer into environment
export FREESURFER_HOME=/home/hexadecagon/Documents/Neuroimaging/freesurfer
export FSFAST_HOME=$FREESURFER_HOME/fsfast
export MNI_DIR=$FREESURFER_HOME/mni
source $FREESURFER_HOME/SetUpFreeSurfer.sh

# Making output directory
mkdir freesurfer_outputs
export SUBJECTS_DIR=freesurfer_outputs 

# Path to image files
INFO_DIR=for_matthew

for subject in $INFO_DIR/*
  do 
  SUBJECT_FOLDER="$(echo $subject | cut -d'/' -f 2)"
  SUBJECT_NAME=str_"$(echo $SUBJECT_FOLDER | cut -d'_' -f 2)".nii.gz
  for file in $INFO_DIR/$SUBJECT_FOLDER/*
# Since the files are not named uniformly, this block detects which of the files is the structural (non-mask) file
    do
      FILE_NAME="$(echo $file | cut -d'/' -f 3)"

      IS_NIFTI=false
      if grep -q ".nii.gz" <<< "$FILE_NAME"; then export IS_NIFTI=true; fi
    
      IS_STR=false
      if grep -q "str" <<< "$FILE_NAME"; then export IS_STR=true; fi

      NOT_MASK=true
      if grep -q "mask" <<< "$FILE_NAME"; then export NOT_MASK=false; fi
    
      if $IS_NIFTI && $IS_STR && $NOT_MASK; then export STR_FILE=$FILE_NAME; break; fi
    done
# Run recon-all
  recon-all -all -s $SUBJECT_FOLDER -i $INFO_DIR/$SUBJECT_FOLDER/$STR_FILE
  echo "Freesurfer recon-all subject $SUBJECT_FOLDER"
  echo $SUBJECT_NAME
done
