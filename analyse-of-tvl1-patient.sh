# bash analyse-syn-patient.sh <patient models dir>

run_evals=1

patientdir=$1

# Make array of patient models, full paths
readarray -t models < <(find $patientdir -mindepth 1 -maxdepth 1 -type d)

for model in ${models[*]}; do
    c="bash analysis-of-tvl1.sh $model"
    if [ $run_evals == 1 ]; then
        eval $c
    fi
done
