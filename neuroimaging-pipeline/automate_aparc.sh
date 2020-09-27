#!/bin/bash

# The second step of the structural pipeline, using aparcstats2table to extract measures to .txt

# Loading freesurfer into environment
export FREESURFER_HOME=/home/hexadecagon/Documents/Neuroimaging/freesurfer
export FSFAST_HOME=$FREESURFER_HOME/fsfast
export MNI_DIR=$FREESURFER_HOME/mni
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export SUBJECTS_DIR=freesurfer_outputs

# Making output directory
mkdir aparc_outputs 

# Path to image files
INFO_DIR=for_matthew

# Get subject identifiers
cd $SUBJECTS_DIR
SUBS=$(ls)
cd ..
echo The directories are $SUBS

# Get stats for all measures and hemispheres
for measure in thickness volume meancurv area
    do 
        for hemisphere in rh lh
            do
                echo ${measure} ${hemisphere}
                aparcstats2table --subjects $SUBS --hemi $hemisphere --parc aparc.a2009s --meas $measure --tablefile aparc_outputs/${measure}_${hemisphere}.txt
            done
    done    
