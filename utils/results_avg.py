import json
import os
import glob
import csv
import time

def load_json_data(file_path):
    json_objects = []
    with open(file_path, 'r') as file:
        content = file.read().strip()
        json_strings = content.split('}\n{')
        for i, json_str in enumerate(json_strings):
            if not json_str.startswith("{"):
                json_str = "{" + json_str
            if not json_str.endswith("}"):
                json_str += "}"
            try:
                json_object = json.loads(json_str)
                json_objects.append(json_object)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON object in file {file_path}: {e}")
    return json_objects

csv_data = []

runs = os.listdir('.')
runs.sort()

for run in runs:
    sum_size_bytes = 0
    sum_duration_seconds = 0
    files = glob.glob(f'./{run}/*.json')
    files.sort()
    for file in files:
        max_retries = 3
        retry_delay = 1
        for attempt in range(max_retries):
            try:
                json_objects = load_json_data(file)
                for data in json_objects:
                    ends = data['end'] if isinstance(data['end'], list) else [data['end']]
                    for end in ends:
                        try:
                            sum_sent = end['sum_sent']
                            sum_size_bytes += sum_sent['bytes']
                            sum_duration_seconds += sum_sent['seconds']
                        except KeyError:
                            print("KeyError")
                break
            except IOError as e:
                print(f"Error opening file {file}: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
        else:
            print(f"Failed to open file {file} after {max_retries} attempts.")

    sum_size_MB = sum_size_bytes / (1024**2)
    avg_speed_Mbps = (sum_size_bytes * 8 / (1024**2)) / sum_duration_seconds if sum_duration_seconds else 0
    row = [run, sum_size_MB, sum_duration_seconds, avg_speed_Mbps]
    csv_data.append(row)

if csv_data:
    avg_size_MB = sum(x[1] for x in csv_data[:-1]) / len(csv_data[:-1])
    avg_duration_seconds = sum(x[2] for x in csv_data[:-1]) / len(csv_data[:-1])
    avg_speed_Mbps = (avg_size_MB * 8) / avg_duration_seconds if avg_duration_seconds else 0
    overall_avg_row = ['Overall', avg_size_MB, avg_duration_seconds, avg_speed_Mbps]
    csv_data.append(overall_avg_row)

with open('results_avg.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Run', 'Total Size (MB)', 'Total Duration (Seconds)', 'Average Speed (Mbps)'])
    writer.writerows(csv_data)
