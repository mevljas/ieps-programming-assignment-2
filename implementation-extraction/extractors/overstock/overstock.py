import re

from util.util import read_file

jewelry_html_1 = read_file("../input-extraction/overstock.com/jewelry01.html")
jewelry_html_2 = read_file("../input-extraction/overstock.com/jewelry02.html")


def regular_expressions() -> None:
    found = re.findall("(?:<body.*?>)([\s\S]*?)(?:<\/body>)", jewelry_html_1)
    print(found)
