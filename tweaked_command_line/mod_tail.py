import subprocess
import argparse
from collections import deque

def tail(file_name, lines):
    with open(file_name, "rb") as file:
        file.seek(0, 2)
        pos = file.tell() # this is like doing len(arr) but for the bytes array that is the file you grabbed its legnth
        # also note that for most simple files this is saying each byte is a character it would be 2 for more complex file types a byte is 8 bits
        result = deque()
        buffer = bytearray()
        while pos > 0 and len(result) < lines:
            pos -= 1
            file.seek(pos)
            byte = file.read(1)
            if b'\n' == byte:
                if buffer:
                    result.appendleft(buffer[::-1].decode())
                    buffer = bytearray()
            else:
                buffer.extend(byte)

        if buffer:
            result.appendleft(buffer[::-1].decode())

    return list(result) 

def inefficient_tail(file, lines):
    result = subprocess.run(["tail", "-n", str(lines), file], capture_output=True, text=True)
    return result.stdout.splitlines()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="description")
    parser.add_argument('--file', required=True)
    parser.add_argument('--lines', type=int, default=10)
    args = parser.parse_args()

    # print(inefficient_tail(args.file, args.lines))
    print("Efficient ------------------")
    for line in inefficient_tail(args.file, args.lines):
        print(line)

    print("Inefficient ------------------")
    for line in tail(args.file, args.lines):
        print(line)
