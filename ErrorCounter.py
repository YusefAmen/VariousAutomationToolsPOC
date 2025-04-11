from collections import Counter
from datetime import datetime
import argparse 

def scan_logs(logfile):
    error_count = 0

    try:
        with open(logfile, "r") as file:
            for line in file:
                if "ERROR" in line:
                    found_time = datetime.now().isoformat() 
                    print(f"[{found_time}] FOUND ERROR: {line.strip()}")
                    error_count += 1

        print(f"\nTotal errors found: {error_count}")

    except FileNotFoundError:
        print(f"❌ File not found: {logfile}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Takes logs and parses for found errors") 
    parser.add_argument("--logfile", type=str, required=True, help="Path to the log file")
    args = parser.parse_args()

    scan_logs(args.logfile)

if __name__ == "__main__":
    main()

