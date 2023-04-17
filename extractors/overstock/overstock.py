import re

from util.util import read_file


def regular_expressions() -> None:
    html = read_file('./pages/overstock.com/jewelry01.html')
    found = re.findall("(?:<body.*?>)([\s\S]*?)(?:<\/body>)", html)
    print(found)
