import sys

from extractors.overstock import overstock
from extractors.rtvslo import rtvslo
from extractors.fri import fri


def main() -> None:
    if len(sys.argv) != 2:
        print("Wrong number of command line arguments.", file=sys.stderr)
        return
    _, algorithm = sys.argv
    match algorithm:
        case 'A':
            overstock.run_regular_expressions()
            rtvslo.run_regular_expressions()
            fri.run_regular_expressions()
        case 'B':
            overstock.run_xpath()
            rtvslo.run_xpath()
            fri.run_xpath()
        case 'C':
            print("Not yet implemented.", file=sys.stderr)
        case _:
            print("Unsupported algorithm type provided.", file=sys.stderr)


if __name__ == "__main__":
    main()
