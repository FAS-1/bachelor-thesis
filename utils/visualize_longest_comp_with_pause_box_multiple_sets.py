import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import numpy as np
from collections import defaultdict

def generate_combined_box_plot(base_folder, set_names, output_file):
    experiment_data = defaultdict(list)
    rr_sjf_data = defaultdict(list)

    for set_name in set_names:
        set_path = os.path.join(base_folder, set_name)

        for experiment_dir in os.listdir(set_path):
            experiment_path = os.path.join(set_path, experiment_dir)
            if os.path.isdir(experiment_path):
                csv_file = os.path.join(experiment_path, 'result_average_longest_completion_time_with_pause.csv')
                if os.path.isfile(csv_file):
                    df = pd.read_csv(csv_file)
                    if 'Longest Completion Time (seconds)' in df.columns:
                        average_completion_time = df['Longest Completion Time (seconds)'].mean()
                        experiment_data[experiment_dir].append(average_completion_time)
                        if experiment_dir.startswith('prio') or experiment_dir.startswith('sjf'):
                            rr_sjf_data[experiment_dir].append(average_completion_time)

    sorted_experiment_keys = sorted(experiment_data.keys())
    data_to_plot = [experiment_data[key] for key in sorted_experiment_keys]

    sorted_rr_sjf_keys = sorted(rr_sjf_data.keys())
    rr_sjf_to_plot = [rr_sjf_data[key] for key in sorted_rr_sjf_keys]

    fig, axs = plt.subplots(2, 1, figsize=(15, 20))

    axs[0].boxplot(data_to_plot, labels=sorted_experiment_keys, vert=True, patch_artist=True)
    axs[0].set_title('Distribution of Average Longest Completion Times across All Experiments')
    axs[0].set_ylabel('Time (seconds)')
    axs[0].set_xlabel('Experiment')
    axs[0].tick_params(axis='x', rotation=45)

    axs[1].boxplot(rr_sjf_to_plot, labels=sorted_rr_sjf_keys, vert=True, patch_artist=True)
    axs[1].set_title('Distribution of Average Longest Completion Times for prio and sjf Experiments')
    axs[1].set_ylabel('Time (seconds)')
    axs[1].set_xlabel('Experiment')
    axs[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script_name.py <base_folder> <output_file_path> <set_name_1> <set_name_2> ...")
        sys.exit(1)

    base_folder = sys.argv[1]
    output_file = sys.argv[2]
    set_names = sys.argv[3:]
    generate_combined_box_plot(base_folder, set_names, output_file)
