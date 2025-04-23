import re
import argparse
from collections import defaultdict
import heapq

def streaming_freq_error(file_name, n):
    result = defaultdict(int)
    ranking = []
    with open(file_name, "r") as file:
        for line in file:
            pattern = r'^\[ERROR\]\s+(?P<msg>.*)'
            cap = re.match(pattern, line)
            if cap:
                error_msg = cap.group("msg")
                print(f"ERROR line: {error_msg}")
                result[error_msg] += 1

                if len(ranking) < n:
                    heapq.heappush(ranking, (result[error_msg], error_msg))
                else:
                    if ranking[0][0] < result[error_msg]:
                        heapq.heappop(ranking)
                        heapq.heappush(ranking, (result[error_msg], error_msg))
    return sorted(ranking, key=lambda x:x[0], reverse=True)


def freq_error(file_name, n): # memory in effecient
    result = defaultdict(int)
    ranking = []
    with open(file_name, "r") as file:
        for line in file:
            pattern = r'^\[ERROR\]\s+(?P<msg>.*)'
            cap = re.match(pattern, line)
            if cap:
                error_msg = cap.group("msg")
                print(f"ERROR line: {error_msg}")
                result[error_msg] += 1

    print(result)
    print(sorted(result.items(), key=lambda x:x[1], reverse=True)[:n]) # this is ineffecient when could do a heapq to keep track of rank
    # could also do a heapq.nlargest(n, result.items(), key=lambda x:x[1])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_name', type=str, required=True)
    parser.add_argument('-n', type=int, required=True)
    args = parser.parse_args()
    try:
        freq_error(args.file_name, args.n)
        print("--------------------------------")
        print(streaming_freq_error(args.file_name, args.n))
    except Exception as e:
        print(f"Exception caught: {e}")
        exit(1)
