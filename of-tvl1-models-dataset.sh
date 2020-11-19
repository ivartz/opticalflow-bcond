run_evals=1

dataset="/mnt/HDD3TB/derivatives/cancer-sim-SAILOR_PROCESSED_MNI-01"

# Make array of patient directories, full paths
readarray -t patients < <(find $dataset -mindepth 1 -maxdepth 1 -type d | sort)

for patient in ${patients[*]}; do
    c="bash of-tvl1-models-patient.sh $patient"
    if [ $run_evals == 1 ]; then
        eval $c
    fi
done
