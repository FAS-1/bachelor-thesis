import json
import glob
import csv
import os

def process_json_object(json_object):
    if "end" in json_object and "sum_sent" in json_object["end"]:
        return json_object["end"]["sum_sent"].get("seconds", 0)
    return 0

def process_file(file_path):
    total_duration = 0
    with open(file_path, 'r') as file:
        content = file.read().strip()
        json_strings = content.replace('}\n{', '}|{').split('|')
        for json_str in json_strings:
            try:
                json_object = json.loads(json_str.strip())
                duration = process_json_object(json_object)
                total_duration += duration
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON object in file {file_path}: {e}")
    return total_duration

def calculate_and_write_average_completion_time():
    runs = [run for run in os.listdir('.') if os.path.isdir(run)]
    runs.sort()

    total_durations = []
    total_counts = []
    for run in runs:
        files = glob.glob(f'./{run}/*.json')
        files.sort()
        run_total_duration = sum(process_file(file_path) for file_path in files)
        total_durations.append(run_total_duration)
        total_counts.append(len(files))

    run_averages = [total / count if count > 0 else 0 for total, count in zip(total_durations, total_counts)]
    overall_average = sum(run_averages) / len(run_averages) if run_averages else 0

    with open('result_average_completion_time.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Run', 'Average Completion Time (seconds)'])
        for i, average in enumerate(run_averages, start=1):
            writer.writerow([f'Run {i}', average])
        writer.writerow(['Overall Average', overall_average])

    print(f"Overall Average Completion Time Per Run: {overall_average} seconds")

calculate_and_write_average_completion_time()
