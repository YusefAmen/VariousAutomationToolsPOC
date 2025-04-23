import requests
import argparse
import re

def getMetricCounts():
    return

def main(logfile):
    with open(logfile, "r") as file:
        for line in file:
            print(f"Line from file: {line}")

            match = re.match(r'myapp_http_requests_total\{status="(\d+)"\}\s+(\d+)', line)

            if match:
                status_code = match.group(1)  # "500"
                count = int(match.group(2))   # 12


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Give me the log file you want to probe. --logfile")
    parser.add_argument("--logfile", type=str, help="give me the logfile")
    args = parser.parse_args()

    main(args.logfile)

    url = "http://localhost:8080/metrics"
    getMetricCounts(url)
