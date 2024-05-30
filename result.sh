#!/bin/bash
set -u

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <Set-Nr.>"
  exit 1
fi

SET=$1
BASE_DIR=~/bachelor-thesis-main/experiments/results/$SET

if [[ ! -d "$BASE_DIR" ]]; then
  echo "The directory $BASE_DIR does not exist."
  exit 1
fi

for dir in $BASE_DIR/*/
do
  if [[ -d "$dir" ]]; then
    echo "Processing directory: $dir"
    cd "$dir"

    rm -f results_*.csv
    rm -f result_*.csv

    python3 ~/bachelor-thesis-main/utils/results_avg.py || { echo "Failed: results_avg.py"; exit 1; }
    python3 ~/bachelor-thesis-main/utils/average_completion_time_without_pause.py || { echo "Failed: average_completion_time_without_pause.py"; exit 1; }
    python3 ~/bachelor-thesis-main/utils/average_longest_completion_time_without_pause.py || { echo "Failed: average_longest_completion_time_without_pause.py"; exit 1; }
    python3 ~/bachelor-thesis-main/utils/average_longest_completion_time_with_pause.py || { echo "Failed: average_longest_completion_time_with_pause.py"; exit 1; }

    pwd
    cat results_*.csv

    cd ~/bachelor-thesis-main/
  else
    echo "Skipping non-existent directory: $dir"
  fi
done

exit 0

