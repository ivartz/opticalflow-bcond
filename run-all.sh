# Transfer over farneback files

dataset="/mnt/HDD3TB/derivatives/cancer-sim-SAILOR_PROCESSED_MNI-01"

#bash of-farneback-models-dataset.sh
#bash of-ilk-models-dataset.sh
#bash of-tvl1-models-dataset.sh

analyse-of-farneback-dataset.sh
analyse-of-ilk-dataset.sh
analyse-of-tvl1-dataset.sh

bash collect-of-farneback-estimation-error-segments.sh 0 > $dataset/syn-of-farneback-estimation-error-segments.txt
bash collect-of-ilk-estimation-error-segments.sh 0 > $dataset/syn-of-ilk-estimation-error-segments.txt
bash collect-of-tvl1-estimation-error-segments.sh 0 > $dataset/syn-of-tvl1-estimation-error-segments.txt

bash collect-of-farneback-estimation-error-segments.sh 1 > $dataset/syn-of-farneback-estimation-error-relative-segments.txt
bash collect-of-ilk-estimation-error-segments.sh 1 > $dataset/syn-of-ilk-estimation-error-relative-segments.txt
bash collect-of-tvl1-estimation-error-segments.sh 1 > $dataset/syn-of-tvl1-estimation-error-relative-segments.txt
