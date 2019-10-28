#!/bin/bash
set -e
max_resolution=$((16*1024))
min_resolution=64

resolution=$max_resolution
resolutions=""
samples=""
while [[ $resolution -ge $min_resolution ]];
do
    echo $resolution
    resolutions="$resolution $resolutions"
    resolution=$(($resolution/2))
    samples="$((2*${max_resolution})) $samples"
done

python ../../tools/make_resolutions_perturbations.py \
       --config template/shock_location.xml \
       --resolutions $resolutions \
       --perturbations 1 \
       --samples $samples \
       --full_time_average
