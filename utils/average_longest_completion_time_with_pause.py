import json
import glob
import csv
import os


def process_json_object(json_object, is_first=False, is_last=False):
    try:
        if "start" in json_object and "end" in json_object:

            if "timestamp" in json_object["start"]:
                start_time = json_object["start"]["timestamp"].get("timesecs", 0)
                duration = json_object["end"]["sum_sent"].get("seconds", 0)
                end_time = start_time + duration if duration else None
                return start_time, end_time
            else:
                print("Warning: 'timestamp' key not found. Setting start_time to 0.")
                start_time = 0
                duration = json_object["end"]["sum_sent"].get("seconds", 0)
                end_time = start_time + duration if duration else None
                return start_time, end_time
        return None, None
    except KeyError as e:
        print(f"KeyError encountered: {e}. JSON object: {json_object}")
        return None, None


def process_file(file_path):
    times = []
    with open(file_path, 'r') as file:
        content = file.read()
        json_strings = content.strip().split('\n}\n{')

        if len(json_strings) == 1:
            try:
                json_object = json.loads(content)
                start_time, end_time = process_json_object(json_object)
                if start_time and end_time:
                    return end_time - start_time
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON object in file {file_path}: {e}")
        else:
            for i, json_str in enumerate(json_strings):
                if not json_str.startswith("{"):
                    json_str = "{" + json_str
                if not json_str.endswith("}"):
                    json_str += "}"
                try:
                    json_object = json.loads(json_str)
                    start_time, end_time = process_json_object(json_object, is_first=(i == 0),
                                                               is_last=(i == len(json_strings) - 1))
                    if start_time is not None and end_time is not None:
                        times.append((start_time, end_time))
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON object in file {file_path}: {e}")
            if times:
                earliest_start = times[0][0]
                latest_end = times[-1][1]
                return latest_end - earliest_start

    return 0


def calculate_and_write_average_longest_completion_time():
    runs = [run for run in os.listdir('.') if os.path.isdir(run)]
    runs.sort()

    longest_completion_times = []

    for run in runs:
        files = glob.glob(f'./{run}/*.json')
        files.sort()
        run_durations = [process_file(file_path) for file_path in files]

        if run_durations:
            longest_duration = max(run_durations)
            longest_completion_times.append(longest_duration)

    overall_average = sum(longest_completion_times) / len(longest_completion_times) if longest_completion_times else 0

    with open('result_average_longest_completion_time_with_pause.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Run', 'Longest Completion Time (seconds)'])
        for i, duration in enumerate(longest_completion_times, 1):
            writer.writerow([f'Run {i}', duration])
        writer.writerow(['Overall Average', overall_average])

    print(f"Overall Average Longest Completion Time With Pause: {overall_average} seconds")


calculate_and_write_average_longest_completion_time()
