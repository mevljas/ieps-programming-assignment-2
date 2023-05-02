import sys

from extractors import overstock
from extractors import rtvslo
from extractors import fri


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
            overstock.run_road_runner()
            rtvslo.run_road_runner()
            fri.run_road_runner()
        case _:
            print("Unsupported algorithm type provided.", file=sys.stderr)


if __name__ == "__main__":
    main()
