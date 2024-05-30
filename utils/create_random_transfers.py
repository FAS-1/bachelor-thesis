import csv
import random


def generate_transfers_csv(num_transfers, filename="transfers.csv"):

    hosts = [f"h{i}" for i in range(10)]

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Source", "Destination", "Data Size (MB)"])

        for _ in range(num_transfers):
            host1, host2 = random.sample(hosts, 2)
            data_size = random.randint(100, 2048)
            writer.writerow([host1, host2, data_size])

    print("Transfers successfully written to", filename)


generate_transfers_csv(20)
