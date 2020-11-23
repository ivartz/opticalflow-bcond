: '
bash collect-of-farneback-estimation-error-segments.sh 0 > syn-of-farneback-estimation-error-segments.txt
'
dataset="/mnt/HDD3TB/derivatives/cancer-sim-SAILOR_PROCESSED_MNI-01"

res="offarneback"
if [ $1 -eq 0 ]; then
    resfile="median-normnegdiff-segmentation.txt"
elif [ $1 -eq 1 ]; then
    resfile="median-normnegdiff-relative-segmentation.txt"
fi

readarray -t errorfiles < <(find $dataset -type f -wholename *$res/$resfile | sort)

echo $(printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "patient" "model" "disp" "grange" "idf" "vecs" "angle" "splo" "sm" "pres" "pabs" "necrosis" "edema" "enhancing")

for errorfile in ${errorfiles[*]}; do
    model=$(dirname $(dirname $errorfile))
    params="$model/params.txt"    
    IFS="=" # Internal Field Separator, used for word splitting
    while read -r param values; do
        readarray -d " " $param < <(echo -n $values)
    done < $params # < creates input stream from file
    modelfolder=$(basename $model)
    patientfolder=$(basename $(dirname $model))
    echo $(printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" $patientfolder $modelfolder ${displacement[0]} ${gaussian_range_one_sided[0]} ${intensity_decay_fraction[0]} ${num_vecs[0]} ${angle_thr[0]} ${spline_order[0]} ${smoothing_std[0]} ${perlin_noise_res[0]} ${perlin_noise_abs_max[0]} $(sed -n 1p $errorfile | tr -d " ") $(sed -n 2p $errorfile | tr -d " ") $(sed -n 3p $errorfile | tr -d " "))
done
