import re
import argparse
from collections import defaultdict
import os
import json

def parse_log(file_name):
    result = defaultdict(lambda: defaultdict(int))
    with open(file_name, "r") as file:
        # parse out the host names in the file and increment counters for given status codes and add to default dictionary 
        for line in file:
            print(f"Line in question: {line}")
            match = re.match(r'^\S+\s+\S+\s+(\S+)\s+\S+\s+\S+\s+(\d{3})$', line)
            if match:
                print("Match found and specific items pulled: ", match.groups())
                host = match.groups()[0]
                status_code = match.groups()[1]
                
                #{host1 : {200 : 1, 500 : 3} }
                result[host][status_code] += 1

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="description")
    parser.add_argument('--file_name', type=str, required=True, help="Please provide the --file_name flag and a valid vile")

    args = parser.parse_args()
    
    file_name = args.file_name
    if not os.path.isfile(file_name):
        print("Invalid file")
        exit(1)

    try:
        print(json.dumps(parse_log(args.file_name), indent=2))
    except Exception as e:
        print(f"Error parsing log: {e}")


