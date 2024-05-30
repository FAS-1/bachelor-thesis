import os
import time
import json
from mininet.log import lg
import ipmininet
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo


class Topo(IPTopo):
    def build(self, *args, **kwargs):
        hosts = []

        for i in range(10):
            host = self.addRouter(f'h{i}')
            hosts.append(host)

        self.addLink(hosts[0], hosts[7], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[0], hosts[5], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[0], hosts[8], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[1], hosts[8], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[2], hosts[4], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[2], hosts[1], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[2], hosts[6], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[3], hosts[9], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[4], hosts[3], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[4], hosts[6], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[5], hosts[8], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[5], hosts[9], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[6], hosts[9], igp_metric=1000, bw=200, delay="5ms")

        self.addLink(hosts[7], hosts[3], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[7], hosts[1], igp_metric=1000, bw=200, delay="5ms")

        # LongestPathFirst
        self.addLink(hosts[3], hosts[8], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[0], hosts[4], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[7], hosts[6], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[2], hosts[5], igp_metric=1000, bw=200, delay="5ms")
        self.addLink(hosts[1], hosts[9], igp_metric=1000, bw=200, delay="5ms")

        return hosts


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
                        received_bytes = last_json['end']['sum_sent'].get('bytes', 0)
                        bytes_transferred_mb = received_bytes / 1024 / 1024
                        return bytes_transferred_mb
                except json.JSONDecodeError:
                    continue

            attempt += 1
            time.sleep(1)
            print("Reading JSON failed! Retrying!")

        except FileNotFoundError:
            return 'File not found.'
        except Exception as e:
            if attempt == max_retries - 1:
                return f'An unexpected error occurred: {e}'
            attempt += 1

    return 'No valid JSON object with the required structure was found after retries.'


tasks = {
    'h2': [('h8', 666), ('h1', 1157), ('h5', 1293)],
    'h7': [('h5', 404), ('h9', 1410), ('h6', 1736)],
    'h6': [('h2', 975), ('h7', 1374), ('h3', 1865), ('h8', 1902)],
    'h4': [('h8', 629)],
    'h0': [('h7', 270)],
    'h3': [('h4', 988), ('h7', 1399)],
    'h8': [('h9', 1916)],
    'h1': [('h2', 398)],
    'h5': [('h4', 323), ('h9', 435), ('h1', 1007), ('h0', 1266)]
}


def initialize_remaining_data(tasks):
    remaining_data = {}
    for source, dests in tasks.items():
        remaining_data[source] = {dest[0]: dest[1] for dest in dests}
    return remaining_data


def perfTestRoundRobin(net, tasks):
    hosts = net.routers
    if not hosts:
        print("Error: Hosts list is empty. Exiting.")
        return

    results_dir = "experiments/results"
    os.makedirs(results_dir, exist_ok=True)

    print("*** Waiting for network to start")
    for i in range(20, 0, -1):
        print(f"{i} ", end="\r", flush=True)
        time.sleep(1)

    print("*** Testing bandwidth between hosts")
    remaining_data = initialize_remaining_data(tasks)

    data_to_transfer_exists = lambda: any(
        any(data_left > 0 for data_left in host_data.values()) for host_data in remaining_data.values())

    while data_to_transfer_exists():
        for host in hosts:
            if host.name not in remaining_data or not any(remaining_data[host.name].values()):
                continue

            for dest_host_name, data_left in remaining_data[host.name].items():
                if data_left <= 0:
                    continue

                dest_host = next((h for h in hosts if h.name == dest_host_name), None)
                if not dest_host:
                    print(f"Destination host {dest_host_name} not found for {host.name}, skipping.")
                    continue

                dest_host.cmd(f'iperf3 -s -p 5000 &')

                result_file = f'{results_dir}/{host.name}_to_{dest_host.name}.json'
                host.cmd(f'iperf3 -c {dest_host} -p 5000 -n {data_left}M -J --logfile {result_file} &')

                time.sleep(10)
                dest_host.cmd('killall iperf3')

                # Retry logic
                retry_attempts = 3
                for attempt in range(retry_attempts):
                    last_json_object = find_last_json_object(result_file)
                    if last_json_object:
                        transferred_megabytes = last_json_object
                        remaining_data[host.name][dest_host_name] -= transferred_megabytes
                        print(
                            f"{host.name} transferred {transferred_megabytes} MB to {dest_host.name}. Remaining: {remaining_data[host.name][dest_host_name]} MB")
                        break
                    else:
                        print(
                            f"Attempt {attempt + 1} failed to parse result for {host.name} to {dest_host.name}. Retrying...")
                        time.sleep(2)
                else:
                    print(
                        f"Failed to parse result after {retry_attempts} attempts for {host.name} to {dest_host.name}. Skipping this host.")

    print("*** All traffic flows initiated and completed")

    print("*** Cleanup completed, stopping network.")
    for host in hosts:
        host.cmd('killall -q iperf3')


ipmininet.DEBUG_FLAG = True
lg.setLogLevel("info")

net = IPNet(topo=Topo(), use_v6=False)
try:
    net.start()
    perfTestRoundRobin(net, tasks)
finally:
    net.stop()
    print("*** Network stopped")
