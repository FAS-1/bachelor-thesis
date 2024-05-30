#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <set_name>"
    exit 1
fi

SET_NAME=$1
BASE_FOLDER=~/bachelor-thesis-main/experiments/results/

OUTPUT_FILE_WITH_PAUSE="${BASE_FOLDER}${SET_NAME}_with_pause.pdf"
OUTPUT_FILE_WITHOUT_PAUSE="${BASE_FOLDER}${SET_NAME}_without_pause.pdf"

cd ~/bachelor-thesis-main/utils/


python3 visualize_longest_comp_with_pause_box.py "$BASE_FOLDER" "$SET_NAME" "$OUTPUT_FILE_WITH_PAUSE"

python3 visualize_longest_comp_without_pause_box.py "$BASE_FOLDER" "$SET_NAME" "$OUTPUT_FILE_WITHOUT_PAUSE"
