run_evals=1

patientdir=$1
fixedimg="$patientdir/T1c.nii.gz"
oftype="oftvl1"

# Make array of patient models, full paths
readarray -t models < <(find $patientdir -mindepth 1 -maxdepth 1 -type d | sort)

for model in ${models[*]}; do
    outdir="$model/$oftype"
    c="mkdir -p $outdir"
    if [ $run_evals == 1 ]; then
        eval $c
    fi
    movingimg="$model/warped.nii.gz"
    c="python3 of-tvl1.py $movingimg $fixedimg $outdir/neg-flow.nii.gz"
    if [ $run_evals == 1 ]; then
        eval $c
    fi
done
