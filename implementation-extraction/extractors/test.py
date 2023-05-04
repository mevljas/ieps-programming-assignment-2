import re
import json

from bs4 import BeautifulSoup
from lxml import etree
from extractors.helpers.helper import read_file
from road_runner.road_runner import road_runner

html_1 = read_file("../input-extraction/test/page1.html", "cp1252")
html_2 = read_file("../input-extraction/test/page2.html", "cp1252")


def run_road_runner() -> None:
    road_runner(first_html=html_1, second_html=html_2)
