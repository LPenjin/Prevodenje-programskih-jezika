import sys

def get_input():
    l = []
    for line in sys.stdin:
        l.append(line)
    return l

def main():
    l = get_input()

    l = [line.strip() for line in l]
    l.append('')

if __name__ == "__main__":
    main()