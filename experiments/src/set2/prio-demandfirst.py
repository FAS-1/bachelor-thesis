import os
import time
import json
import threading
import subprocess
from mininet.log import lg
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo


class Topo(IPTopo):
    def build(self, *args, **kwargs):
        hosts = []

        for i in range(10):
            host = self.addRouter(f'h{i}')
            hosts.append(host)

        self.addLink(hosts[0], hosts[9], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[1], hosts[5], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[1], hosts[3], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[1], hosts[9], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[2], hosts[4], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[2], hosts[0], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[2], hosts[8], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[3], hosts[7], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[3], hosts[6], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[4], hosts[6], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[4], hosts[8], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[5], hosts[7], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[5], hosts[9], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[6], hosts[0], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[7], hosts[8], igp_metric=1000, bw=200, delay="5ms")

        # DemandFirst
        self.addLink(hosts[9], hosts[7], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[3], hosts[8], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[4], hosts[1], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[2], hosts[6], igp_metric=1000, bw=200, delay="5ms")

        return hosts


def initialize_tasks():
    tasks = {
        'h9': [('h0', 772, 4), ('h2', 1458, 4)],
        'h7': [('h4', 356, 5), ('h9', 867, 5)],
        'h6': [('h3', 271, 4), ('h2', 1835, 3)],
        'h4': [('h5', 184, 1), ('h7', 1387, 5)],
        'h0': [('h6', 1458, 4)],
        'h8': [('h1', 1105, 3), ('h4', 1335, 2)],
        'h1': [('h5', 812, 5), ('h3', 1057, 3), ('h2', 1339, 4), ('h7', 1828, 2), ('h0', 1971, 5)],
        'h5': [('h8', 922, 5), ('h1', 1152, 3)],
        'h2': [('h7', 403, 3), ('h3', 1381, 2)]
    }
    return tasks


def check_iperf_completion(file_path, timeout=300):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if not os.path.exists(file_path):
            time.sleep(1)
            continue
        with open(file_path, 'r') as file:
            try:
                content = file.read().strip()
                if content:
                    json_data = json.loads(content)
                    if json_data.get("end"):
                        return True
            except json.JSONDecodeError:
                pass
        time.sleep(1)
    return False

def find_last_json_object(file_path, max_retries=10):
    attempt = 0
    while attempt < max_retries:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().rstrip()

            brace_count = 0
            json_objects = []
            temp_str = ''

            for char in content:
                if char == '{':
                    brace_count += 1
                if brace_count > 0:
                    temp_str += char
                if char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_objects.append(temp_str)
                        temp_str = ''

            for json_str in reversed(json_objects):
                try:
                    last_json = json.loads(json_str)
                    if 'end' in last_json and 'sum_sent' in last_json['end']:
                        received_bytes = int(last_json['end']['sum_sent'].get('bytes', 0))
                        bytes_transferred_mb = received_bytes / 1024 / 1024
                        return bytes_transferred_mb
                except json.JSONDecodeError:
                    continue

            attempt += 1
            time.sleep(1)
            print("Reading JSON failed! Retrying!")

        except FileNotFoundError:
            return 0
        except Exception as e:
            if attempt == max_retries - 1:
                return 0
            attempt += 1

    return 0

def initialize_remaining_data(tasks):
    remaining_data = {}
    for source, dests in tasks.items():
        remaining_data[source] = {dest[0]: dest[1] for dest in dests}
    return remaining_data

class TaskManager:
    def __init__(self):
        self.ready_queue = []
        self.current_task = None
        self.lock = threading.Lock()

    def add_task(self, task):
        with self.lock:
            print(f"Adding task {task.source_name} to {task.dest_name} with priority {task.priority}")
            if self.current_task is None:
                self.current_task = self.create_task_runner(task)
                self.current_task.start()
            elif task.priority < self.current_task.priority:
                print(
                    f"Preempting current task {self.current_task.source_name} to {self.current_task.dest_name} with new higher priority task")
                self.current_task.preempt()
                time.sleep(1)
                self.current_task = self.create_task_runner(task)
                self.current_task.start()
            else:
                if task not in self.ready_queue:
                    self.ready_queue.append(task)
                    self.ready_queue.sort(key=lambda x: x.priority)
            self.show_status()

    def finish_current_task(self):
        with self.lock:
            print(f"Finishing task {self.current_task.source_name} to {self.current_task.dest_name}")
            if self.current_task and self.current_task.data_amount <= 0:
                if self.ready_queue:
                    self.ready_queue.sort(key=lambda x: x.priority)
                    self.current_task = self.create_task_runner(self.ready_queue.pop(0))
                    self.current_task.start()
                else:
                    self.current_task = None
                    print("No more tasks in the queue.")
            else:
                print(f"Task {self.current_task.source_name} to {self.current_task.dest_name} is not yet complete and has {self.current_task.data_amount}MB remaining.")
            self.show_status()

    def create_task_runner(self, task):
        return TaskRunner(task.net, task.source_name, task.dest_name, task.data_amount, task.priority,
                          task.results_dir, task.remaining_data, self)

    def requeue_task(self, task):
        if task.data_amount > 0:
            self.ready_queue.append(task)
            self.ready_queue.sort(key=lambda x: x.priority)

    def show_status(self):
        current = f"Current Task: {self.current_task.source_name} to {self.current_task.dest_name} with remaining {self.current_task.data_amount}MB" if self.current_task else "No task is currently running."
        queue = "Ready Queue: " + ", ".join([f"{t.source_name}->{t.dest_name} (Priority: {t.priority}, Remaining: {t.data_amount}MB)" for t in self.ready_queue])
        print(current)
        print(queue)


class TaskRunner(threading.Thread):

    def __init__(self, net, source_name, dest_name, data_amount, priority, results_dir, remaining_data, task_manager):
        threading.Thread.__init__(self)
        self.net = net
        self.source_name = source_name
        self.dest_name = dest_name
        self.data_amount = data_amount
        self.priority = priority
        self.results_dir = results_dir
        self.result_file = f"{self.results_dir}/{source_name}-{dest_name}.json"
        self.remaining_data = remaining_data
        self.task_manager = task_manager
        self.running = False
        self.process = None
        self.initial_data_amount = data_amount
        self.timeout = 300

    def run(self):
        if self.data_amount > 0:
            self.running = True
            self.start_iperf_task()
            start_time = time.time()
            while self.running:
                if self.check_completion() or (time.time() - start_time >= self.timeout):
                    self.data_amount = 0
                    self.running = False
                time.sleep(1)
            self.task_manager.finish_current_task()

    def notify_completion(self):
        print(f"Task from {self.source_name} to {self.dest_name} has completed all data transfers.")

    def start_iperf_task(self):
        unique_port = 5001 + abs(hash((self.source_name, self.dest_name))) % 999
        dest_router = self.net.get(self.dest_name)
        source_router = self.net.get(self.source_name)

        dest_router.cmd('killall -9 iperf3')
        source_router.cmd('killall -9 iperf3')

        dest_router.cmd(f'iperf3 -s -p {unique_port} &')
        time.sleep(5)

        self.process = source_router.popen(
            f'iperf3 -c {dest_router.IP()} -p {unique_port} -n {self.data_amount}M -J --logfile {self.result_file}',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def check_completion(self):
        complete = check_iperf_completion(self.result_file)
        if complete:
            transferred_mb = find_last_json_object(self.result_file)
            self.data_amount = self.initial_data_amount - transferred_mb
            self.remaining_data[self.source_name][self.dest_name] = self.data_amount
            return self.data_amount <= 0
        return False

    def preempt(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        self.net.get(self.source_name).cmd('killall -9 iperf3')
        self.net.get(self.dest_name).cmd('killall -9 iperf3')
        self.running = False
        transferred = find_last_json_object(self.result_file)
        self.data_amount = self.initial_data_amount - transferred
        print(f"Preempted {self.source_name} to {self.dest_name}, {self.data_amount} MB remaining")
        if self.data_amount > 0:
            time.sleep(2)
            self.task_manager.requeue_task(self)
        else:
            self.notify_completion()

    def calculate_remaining_data(self):
        transferred = find_last_json_object(self.result_file)
        remaining = max(0, self.initial_data_amount - transferred)
        return remaining


def schedule_tasks(net, tasks):
    results_dir = "experiments/results"
    os.makedirs(results_dir, exist_ok=True)
    remaining_data = initialize_remaining_data(tasks)
    task_manager = TaskManager()

    for source, dests in tasks.items():
        for dest, amount, priority in dests:
            task_runner = TaskRunner(net, source, dest, amount, priority, results_dir, remaining_data, task_manager)
            time.sleep(5)
            task_manager.add_task(task_runner)

    while task_manager.current_task or any(t.is_alive() for t in threading.enumerate() if isinstance(t, TaskRunner)):
        time.sleep(1)

    active_threads = [t for t in threading.enumerate() if isinstance(t, TaskRunner)]
    for t in active_threads:
        t.join()

def main():
    lg.setLogLevel('info')
    net = IPNet(topo=Topo(), use_v6=False)
    try:
        net.start()

        print("*** Waiting for network to start")
        for i in range(20, 0, -1):
            print(f"{i}  ", end="\r", flush=True)
            time.sleep(1)

        tasks = initialize_tasks()
        schedule_tasks(net, tasks)
    finally:
        net.stop()
        print("*** Network stopped ***")

if __name__ == '__main__':
    main()
