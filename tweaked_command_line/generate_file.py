def generate_test_file(filename="test_log.txt", lines=1000):
    with open(filename, "w") as f:
        for i in range(1, lines + 1):
            f.write(f"line {i}\n")

if __name__ == "__main__":
    generate_test_file()

