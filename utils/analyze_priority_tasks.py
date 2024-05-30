import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import glob


def parse_json_file_correctly(file_path):
    data_list = []
    with open(file_path, 'r') as file:
        content = file.read()
        json_objects = content.split('}{')
        for obj in json_objects:
            obj = obj.strip()
            if not obj.startswith('{'):
                obj = '{' + obj
            if not obj.endswith('}'):
                obj = obj + '}'
            try:
                data = json.loads(obj)
                if 'start' in data and 'end' in data:
                    if 'timestamp' in data['start']:
                        start_time = data['start']['timestamp']['timesecs']
                    elif 'connected' in data['start']:
                        start_time = data['start']['connected'][0]['timesecs']
                    else:
                        print(f"Unexpected JSON structure for start time in {file_path}")
                        continue
                    finish_time = start_time + data['end']['streams'][0]['sender']['seconds']
                    data_list.append({
                        'Start Time': pd.to_datetime(start_time, unit='s'),
                        'Finish Time': pd.to_datetime(finish_time, unit='s')
                    })
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e} in file {file_path}")
            except KeyError as e:
                print(f"KeyError: {e} in file {file_path}")
    return data_list


# Define paths
json_file_base_path = '/Users/marvin/Documents/GitHub/bachelor-thesis/experiments/results/'  # Base path to your JSON files
csv_file_base_path = '/Users/marvin/Documents/GitHub/bachelor-thesis/experiments/csv/'  # Base path to your CSV files

# Assume we have directories named set1, set2, ..., setN for different experiment sets
experiment_sets = ['set1']  # Add all your experiment set names here

all_normalized_data = []

for exp_set in experiment_sets:
    # Parse JSON files for the current experiment set
    json_file_paths = glob.glob(f'{json_file_base_path}{exp_set}/*.json')
    all_data_list = []
    for file_path in json_file_paths:
        data_list = parse_json_file_correctly(file_path)
        all_data_list.extend(data_list)

    # Debug: Print parsed data
    print(f"Experiment Set: {exp_set}")
    print(f"Parsed Data: {all_data_list[:5]}")  # Print first 5 entries for inspection

    # Convert parsed data to DataFrame
    parsed_data_df = pd.DataFrame(all_data_list)
    parsed_data_df['ID'] = range(len(parsed_data_df))

    # Debug: Print DataFrame structure
    print(f"DataFrame Structure: {parsed_data_df.head()}")

    # Load priority data for the current experiment set
    priority_data = pd.read_csv(f'{csv_file_base_path}prio_transfers_{exp_set}.csv')
    priority_data['ID'] = range(len(priority_data))

    # Merge with priority data
    merged_data = pd.merge(priority_data, parsed_data_df, on='ID', how='outer')

    # Debug: Print merged DataFrame structure
    print(f"Merged DataFrame Structure: {merged_data.head()}")

    # Normalize start and finish times
    min_start_time = merged_data['Start Time'].min()
    merged_data['Normalized Start Time'] = (merged_data['Start Time'] - min_start_time).dt.total_seconds()
    merged_data['Normalized Finish Time'] = (merged_data['Finish Time'] - min_start_time).dt.total_seconds()

    # Debug: Check for unique start and finish times
    print(f"Normalized Start Times for {exp_set}: {merged_data['Normalized Start Time'].unique()}")
    print(f"Normalized Finish Times for {exp_set}: {merged_data['Normalized Finish Time'].unique()}")

    # Add experiment set information
    merged_data['Experiment Set'] = exp_set

    # Append to the list of all normalized data
    all_normalized_data.append(merged_data)

# Combine all normalized data into one DataFrame
if all_normalized_data:
    all_normalized_data_df = pd.concat(all_normalized_data)

    # Plot individual transfers with labels at start and finish times
    fig, ax = plt.subplots(figsize=(14, 10))
    colors = plt.cm.viridis(np.linspace(0, 1, all_normalized_data_df['Priority'].nunique()))

    legend_added = set()

    for priority, group in all_normalized_data_df.groupby('Priority'):
        for _, row in group.iterrows():
            color = colors[priority - 1]
            label = f'Priority {priority}' if priority not in legend_added else ""
            ax.plot([row['Normalized Start Time'], row['Normalized Finish Time']], [priority, priority], color=color,
                    label=label)
            ax.annotate(f"{row['Source']} to {row['Destination']} (Start)",
                        (row['Normalized Start Time'], priority), textcoords="offset points", xytext=(0, -10),
                        ha='center', fontsize=8)
            ax.annotate(f"{row['Source']} to {row['Destination']} (Finish)",
                        (row['Normalized Finish Time'], priority), textcoords="offset points", xytext=(0, 10),
                        ha='center', fontsize=8)
            legend_added.add(priority)

    plt.xlabel('Normalized Time (seconds)')
    plt.ylabel('Priority Levels')
    plt.title('Normalized Start and Finish Times by Priority Across Experiment Sets')
    plt.legend(title='Priority Levels')
    plt.grid(True)
    plt.tight_layout()

    plt.show()
else:
    print("No valid data to plot.")