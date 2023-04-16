import sys

from extractors.regular_expressions import overstock


def main() -> None:
    if len(sys.argv) != 2:
        print("Wrong number of command line arguments.", file=sys.stderr)
        return
    _, algorithm = sys.argv
    match algorithm:
        case 'A':
            overstock.extract()
        case 'B':
            print("Not yet implemented.", file=sys.stderr)
        case 'C':
            print("Not yet implemented.", file=sys.stderr)
        case _:
            print("Unsupported algorithm type provided.", file=sys.stderr)


if __name__ == "__main__":
    main()
