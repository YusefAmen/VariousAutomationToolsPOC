import time, argparse, psutil
from datetime import datetime


def cpu_monitor(threshold, interval):
    while True:
        usage =  psutil.cpu_percent(interval)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if usage > threshold:
            print(f"[ALERT] The CPU usage was above threshold at {usage}%.")
        else:
            print(f"{now}[INFO] The CPU usage: {usage}%.")
        time.sleep(5)
    
#def memory_monitor(threshold, interval):
#    usage =  psutil.cpu_percent(interval)
#    while True:
#        if usage > threshold:
#            print(f"[ALERT] The Memory usage was above threshold at {usage}%.")
#    time.sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--threshold', type=int, required=True)
    parser.add_argument('--interval', type=int, required=True)
    
    args = parser.parse_args()
    cpu_monitor(args.threshold, args.interval)
