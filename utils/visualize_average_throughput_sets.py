import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
from collections import defaultdict

def generate_combined_box_plot_for_throughput(base_folder, set_names, output_file):
    experiment_data = defaultdict(list)
    rr_prio_data = defaultdict(list)

    for set_name in set_names:
        set_path = os.path.join(base_folder, set_name)

        for experiment_dir in os.listdir(set_path):
            experiment_path = os.path.join(set_path, experiment_dir)
            if os.path.isdir(experiment_path):
                csv_file = os.path.join(experiment_path, 'results_avg.csv')
                if os.path.isfile(csv_file):
                    df = pd.read_csv(csv_file)
                    if 'Average Speed (Mbps)' in df.columns:
                        average_throughput = df['Average Speed (Mbps)'].mean()
                        experiment_data[experiment_dir].append(average_throughput)
                        if experiment_dir.startswith('rr') or experiment_dir.startswith('prio'):
                            rr_prio_data[experiment_dir].append(average_throughput)

    sorted_experiment_keys = sorted(experiment_data.keys())
    data_to_plot = [experiment_data[key] for key in sorted_experiment_keys]

    sorted_rr_prio_keys = sorted(rr_prio_data.keys())
    rr_prio_to_plot = [rr_prio_data[key] for key in sorted_rr_prio_keys]

    fig, axs = plt.subplots(2, 1, figsize=(15, 20))

    axs[0].boxplot(data_to_plot, labels=sorted_experiment_keys, vert=True, patch_artist=True)
    axs[0].set_title('Distribution of Average Throughput across All Experiments')
    axs[0].set_ylabel('Throughput (Mbps)')
    axs[0].set_xlabel('Experiment')
    axs[0].tick_params(axis='x', rotation=45)

    axs[1].boxplot(rr_prio_to_plot, labels=sorted_rr_prio_keys, vert=True, patch_artist=True)
    axs[1].set_title('Distribution of Average Throughput for rr and prio Experiments')
    axs[1].set_ylabel('Throughput (Mbps)')
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
    generate_combined_box_plot_for_throughput(base_folder, set_names, output_file)
