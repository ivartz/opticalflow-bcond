: '
bash analysis.sh <model dir>

Analyse the difference between ground truth (model) displacements and
Iterative Lucas-Kanade optical flow estimated displacement.

For each nonzero tumor segment

Segmentation.nii.gz:

0: Outside of tumor
1: Necrosis
2: Edema
3: Enhancing
'
model=$1
res="ofilk"

# Get parent directory of model directory
patient=$(dirname $model)

# Calculate mean of nonzero absolute error vector values in tumor segments
c="python3 median-nonzero.py $patient/Segmentation.nii.gz $model/$res/normnegdiff.nii.gz > $model/$res/median-normnegdiff-segmentation.txt"
eval $c

# Calculate mean of nonzero relative absolute error vector values in tumor segments
c="python3 median-nonzero.py $patient/Segmentation.nii.gz $model/$res/normnegdiff-relative.nii.gz > $model/$res/median-normnegdiff-relative-segmentation.txt"
eval $c
