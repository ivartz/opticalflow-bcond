# bash analyse-syn-dataset.sh

run_evals=1

dataset="/mnt/HDD3TB/derivatives/cancer-sim-SAILOR_PROCESSED_MNI-01"

# Make array of patient directories, full paths
readarray -t patients < <(find $dataset -mindepth 1 -maxdepth 1 -type d)

num_patients=${#patients[*]}

i=1

for patient in ${patients[*]}; do
    echo "$i/$num_patients"
    c="bash analyse-of-tvl1-patient.sh $patient"
    if [ $run_evals == 1 ]; then
        eval $c
    fi
    i=$(($i+1))
done
