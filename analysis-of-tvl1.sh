: '
bash analysis.sh <model dir>

Analyse the difference between ground truth (model) displacements and
TVL-1 optical flow estimated displacement.

For each nonzero tumor segment

Segmentation.nii.gz:

0: Outside of tumor
1: Necrosis
2: Edema
3: Enhancing
'
model=$1
res="oftvl1"

# Vectors to show the error: GT - estimated displacement
c="fslmaths $model/interp-field-*.*mm.nii.gz -sub $model/$res/flow.nii.gz $model/$res/diff.nii.gz"
eval $c

# Absolute value of error vectors
c="fslmaths $model/$res/diff.nii.gz -sqr -Tmean -mul 3 -sqrt $model/$res/normdiff.nii.gz"
eval $c

# Absolute value of estimated displacement
c="fslmaths $model/interp-field-*.*mm.nii.gz -sqr -Tmean -mul 3 -sqrt $model/$res/normgt.nii.gz"
eval $c

# Relative absolute of error vectors
c="fslmaths $model/$res/normdiff.nii.gz -div $model/$res/normgt.nii.gz $model/$res/normdiff-relative.nii.gz"
eval $c

# Get parent directory of model directory
patient=$(dirname $model)

# Calculate mean of nonzero absolute error vector values in tumor segments
c="fslstats -K $patient/Segmentation.nii.gz $model/$res/normdiff.nii.gz -M > $model/$res/mean-normdiff-segmentation.txt"
eval $c

# Calculate mean of nonzero relative absolute error vector values in tumor segments
c="fslstats -K $patient/Segmentation.nii.gz $model/$res/normdiff-relative.nii.gz -M > $model/$res/mean-normdiff-relative-segmentation.txt"
eval $c
