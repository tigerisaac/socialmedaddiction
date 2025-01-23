# changed to fit with ui instead of as standalone prgrm

import matplotlib.pyplot as plt
from datetime import datetime

def read_log_file(file_path):
    with open(file_path, 'r') as file:
        logs = file.readlines()
    return logs

def filter_logs(logs, websites, ip_address):
    access_counts = {website: [0] * 24 for website in websites}

    for line in logs:
        parts = line.strip().split('|')
        if len(parts) < 3:
            continue

        timestamp_str, client_ip, domain = parts[0], parts[1], parts[2]
        if client_ip != ip_address:
            continue

        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')

        for website in websites:
            if domain.endswith(website):
                hour = timestamp.hour
                access_counts[website][hour] += 1

    return access_counts

def plot_combined_access_data(access_counts):
    plt.figure(figsize=(14, 8))
    hours = range(24)

    for website, counts in access_counts.items():
        plt.plot(hours, counts, marker='o', label=website)

    plt.xlabel("Hour")
    plt.ylabel("Visits")
    plt.title("Visits per Hour")
    plt.xticks(hours)
    plt.yticks(range(0, max(max(counts) for counts in access_counts.values()) + 2, 20)) # change last value for bigger ticks
    plt.legend()
    plt.grid(visible=True, linestyle="--", alpha=0.6)
    return plt
