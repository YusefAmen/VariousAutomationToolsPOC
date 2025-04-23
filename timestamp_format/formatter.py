import datetime
import argparse
import re
import os
import sys
import json

def formatter(input_file):
    formatted_timestamps = []
    re_patterns = [
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z'  
    ]
    datetime_patterns = {
            "iso": 'Y-m-dTHH:M:SZ'  
    }
    with open(input_file, "r") as file:
        data = json.load(file)
        timestamps = data.get("timestamps", [])
        for timestamp in timestamps:
            for i in range(len(re_patterns)):
                if re.match(re_patterns[i], timestamp):
                    print(f"found a match: {timestamp}")
                    print(type(datetime.datetime.strptime(timestamp, datetime_patterns['iso']).strftime("YYYY-MM-DD HH:MM:SS")))


    return formatted_timestamps


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pass a --stamps file json array of timestamps.")
    parser.add_argument('--stamps', required=True, type=str, help='path to json file contianing the timestamps')

    args = parser.parse_args()
    stamps = args.stamps

    if not os.path.isfile(stamps):
        print("invalid file {stamps}")
        sys.exit(1)

    try:
        formatter(stamps)
    except Exception as e:
        print(f"Please provide json file of timestamps. Error: {e}", file=sys.stderr)
        sys.exit(2)
