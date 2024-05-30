#!/bin/bash
set -e

cd ~/bachelor-thesis-main/

for set_dir in experiments/results/*/;
do
  if [ -d "$set_dir" ]; then
    for dir in "$set_dir"*/;
    do
      cd "$dir"

      rm -f results_*.csv
      rm -f result_*.csv

      python3 ~/bachelor-thesis-main/utils/results_avg.py
      python3 ~/bachelor-thesis-main/utils/average_completion_time_without_pause.py
      python3 ~/bachelor-thesis-main/utils/average_longest_completion_time_without_pause.py
      python3 ~/bachelor-thesis-main/utils/average_longest_completion_time_with_pause.py

      pwd

      cat results_*.csv

      cd ~/bachelor-thesis-main/
    done
  fi
done

cd ~/bachelor-thesis-main/utils
python3 visualize_longest_comp_without_pause_box_multiple_sets.py ~/bachelor-thesis-main/experiments/results/ ~/bachelor-thesis-main/experiments/longest_completion_time_without_pause.pdf set1 set2 set3 set4 set5
python3 visualize_longest_comp_with_pause_box_multiple_sets.py ~/bachelor-thesis-main/experiments/results/ ~/bachelor-thesis-main/experiments/longest_completion_time_with_pause.pdf set1 set2 set3 set4 set5
python3 visualize_average_throughput_sets.py ~/bachelor-thesis-main/experiments/results/ ~/bachelor-thesis-main/experiments/average_throughput.pdf set1 set2 set3 set4 set5
exit 0
