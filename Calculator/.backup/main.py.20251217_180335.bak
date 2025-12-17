import sys

def main(a=0, b=0, c=0):
    print("a =", a)
    print("b =", b)
    print("c =", c)

if __name__ == "__main__":
    args = sys.argv[1:]
    args = args if len(args) >= 3 else [0, 0, 0]  # Default to zero if not enough arguments
    main(*args[:3])
