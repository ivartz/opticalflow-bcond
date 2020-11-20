: '
bash analysis.sh <model dir>

Analyse the difference between ground truth (model) displacements and
Farneback optical flow estimated displacement.

For each nonzero tumor segment

Segmentation.nii.gz:

0: Outside of tumor
1: Necrosis
2: Edema
3: Enhancing
'
model=$1
res="offarneback"

# Vectors to show the error: GT - estimated displacement, Opposite direction
c="fslmaths $model/interp-neg-field-*.*mm.nii.gz -sub $model/$res/neg-flow.nii.gz $model/$res/negdiff.nii.gz"
eval $c

# Absolute value of error vectors, opposite
c="fslmaths $model/$res/negdiff.nii.gz -sqr -Tmean -mul 3 -sqrt $model/$res/normnegdiff.nii.gz"
eval $c

# Absolute value of estimated displacement, opposite
c="fslmaths $model/interp-neg-field-*.*mm.nii.gz -sqr -Tmean -mul 3 -sqrt $model/$res/normneggt.nii.gz"
eval $c

# Relative absolute of error vectors, opposite
c="fslmaths $model/$res/normnegdiff.nii.gz -div $model/$res/normneggt.nii.gz $model/$res/normnegdiff-relative.nii.gz"
eval $c

# Get parent directory of model directory
patient=$(dirname $model)

# Calculate mean of nonzero absolute error vector values in tumor segments
c="fslstats -K $patient/Segmentation.nii.gz $model/$res/normnegdiff.nii.gz -M > $model/$res/mean-normnegdiff-segmentation.txt"
eval $c

# Calculate mean of nonzero relative absolute error vector values in tumor segments
c="fslstats -K $patient/Segmentation.nii.gz $model/$res/normnegdiff-relative.nii.gz -M > $model/$res/mean-normnegdiff-relative-segmentation.txt"
eval $c
