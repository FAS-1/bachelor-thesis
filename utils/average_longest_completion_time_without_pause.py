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
        json_strings = content.split('}\n{')
        for i, json_str in enumerate(json_strings):
            if i != 0: json_str = '{' + json_str
            if i != len(json_strings) - 1: json_str += '}'
            try:
                json_object = json.loads(json_str)
                duration = process_json_object(json_object)
                total_duration += duration
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON object in file {file_path}: {e}")

    return total_duration


def calculate_and_write_average_longest_completion_time():
    runs = [run for run in os.listdir('.') if os.path.isdir(run)]
    runs.sort()

    run_longest_durations = []
    for run in runs:
        files = glob.glob(f'./{run}/*.json')
        files.sort()
        longest_run_duration = max(process_file(file_path) for file_path in files)
        run_longest_durations.append(longest_run_duration)

    if run_longest_durations:
        average_longest_completion_time = sum(run_longest_durations) / len(run_longest_durations)
    else:
        average_longest_completion_time = 0

    with open('result_average_longest_completion_time_without_pause.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Run', 'Longest Completion Time (seconds)'])
        for i, duration in enumerate(run_longest_durations, start=1):
            writer.writerow([f'Run {i}', duration])
        writer.writerow(['Overall Average', average_longest_completion_time])

    print(f"Average Longest Completion Time Without Pause: {average_longest_completion_time} seconds")


calculate_and_write_average_longest_completion_time()
