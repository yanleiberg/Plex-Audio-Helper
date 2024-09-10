def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}:{milliseconds:03d}"

def time_to_seconds(time_str):
    h, m, s, ms = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s + ms / 1000

import os
import psutil

def is_ssd(path):
    try:
        disk = psutil.disk_partitions()
        for partition in disk:
            if os.path.commonpath([path, partition.mountpoint]) == partition.mountpoint:
                return "SSD" in partition.opts.upper() or "NVME" in partition.device.upper()
    except:
        pass
    return False

import json
import os

def save_settings(settings, filename='config/settings.json'):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(settings, f, indent=2)
    print(f"Settings saved to {filename}")
    print(f"Saved settings content: {json.dumps(settings, indent=2)}")

def load_settings(filename='config/settings.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            settings = json.load(f)
        print(f"Settings loaded from {filename}")
        print(f"Loaded settings content: {json.dumps(settings, indent=2)}")
        return settings
    return {}


