import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import numpy as np

def generate_combined_box_plot(base_folder, set_name, output_file):
    data_to_plot = []
    labels = []

    set_path = os.path.join(base_folder, set_name)

    for experiment_dir in os.listdir(set_path):
        experiment_path = os.path.join(set_path, experiment_dir)
        if os.path.isdir(experiment_path):
            csv_file = os.path.join(experiment_path, 'result_average_longest_completion_time_with_pause.csv')
            if os.path.isfile(csv_file):
                df = pd.read_csv(csv_file)
                if 'Longest Completion Time (seconds)' in df.columns:
                    data_to_plot.append(df['Longest Completion Time (seconds)'].tolist())
                    labels.append(experiment_dir)

    if data_to_plot and labels:
        plt.figure(figsize=(10, 6))
        plt.boxplot(data_to_plot, labels=labels, vert=True, patch_artist=True)
        plt.title(f'Comparison of Longest Completion Times across Experiments ({set_name})')
        plt.ylabel('Time (seconds)')
        plt.xlabel('Experiment')
        plt.xticks(rotation=45)

        y_min = min(min(data) for data in data_to_plot if data)
        y_max = max(max(data) for data in data_to_plot if data)
        tick_interval = 15
        plt.yticks(np.arange(y_min, y_max + tick_interval, tick_interval))

        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        print(f"Plot saved to {output_file}")
    else:
        print("No data available for plotting.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script_name.py <base_folder> <set_name> <output_file_path>")
        sys.exit(1)

    base_folder = sys.argv[1]
    set_name = sys.argv[2]
    output_file = sys.argv[3]
    generate_combined_box_plot(base_folder, set_name, output_file)
