import re
import json

from bs4 import BeautifulSoup
from lxml import etree
from extractors.helpers.helper import read_file
from road_runner.road_runner import start_running

# on macOS, the following encoding is needed to read the files: "cp1252"
jewelry_html_1 = read_file("../input-extraction/overstock.com/jewelry01.html", "cp1252")
jewelry_html_2 = read_file("../input-extraction/overstock.com/jewelry02.html", "cp1252")


def regular_expressions(html) -> None:
    # Title
    titles_regex = r'<td valign="top">[\n\s]*?<a\s.*?><b>(.*?)</b></a>'
    titles = re.findall(titles_regex, html)

    # List Price
    list_price_regex = r'<td align="left"\s.*?>[\n\s]*?<s>(.*?)</s>'
    list_prices = re.findall(list_price_regex, html)

    # Price
    price_regex = r'<td align="left"\s.*?>[\n\s]*?<span class="bigred"><b>(.*?)</b></span>'
    prices = re.findall(price_regex, html)

    # Saving and Saving Percent
    saving_regex = r'<td align="left"\s.*?>[\n\s]*?<span class="littleorange">(\$.*?)\s\((.*?)\)</span>'
    savings = re.findall(saving_regex, html)

    # Content
    content_regex = r'<span class="normal">([\S\s]*?)[\s]*<br>'
    contents = re.findall(content_regex, html)

    # check for missing values
    if not (len(titles) == len(list_prices) == len(prices) == len(savings) == len(contents)):
        print("Missing values in titles or list prices.")
        return

    # construct JSON object with extracted data
    data = []
    for i in range(len(titles)):
        data.append({
            "Title": titles[i],
            "ListPrice": list_prices[i],
            "Price": prices[i],
            "Saving": savings[i][0],
            "SavingPercent": savings[i][1],
            "Content": contents[i].replace("\n", " ").strip()  # prettify text
        })

    # output JSON 
    print(json.dumps(data, indent=4))


def xpath(html) -> None:
    soup = BeautifulSoup(html, 'html.parser')
    dom = etree.HTML(str(soup))

    items = dom.xpath(
        '/html/body/table[2]/tbody/tr[1]/td[5]/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[@bgcolor]')
    data = []

    for item in items:
        # Title
        title = item.xpath('./td[2]/a/b/text()')
        # if missing title then item is not jewelry
        if not title:
            continue
        title = title[0]

        # List Price
        list_price = item.xpath('./td[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/s/text()')[0]

        # Price
        price = item.xpath('./td[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/span/b/text()')[0]

        # Saving and Saving Percent
        saving_and_saving_percent = item.xpath('./td[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span/text()')[0]
        saving = saving_and_saving_percent.split("(")[0].strip()
        saving_percent = saving_and_saving_percent.split("(")[1].split(")")[0].strip()

        # Content
        content = item.xpath('./td[2]/table/tbody/tr/td[2]/span/text()')[0]
        # remove everything after <br tag (anchor tags, spans, etc.) and replace newlines inside the text
        content = content.split("<br")[0].replace("\n", " ").strip()

        # construct JSON object with extracted data
        data.append({
            "Title": title,
            "ListPrice": list_price,
            "Price": price,
            "Saving": saving,
            "SavingPercent": saving_percent,
            "Content": content
        })

    # output JSON 
    print(json.dumps(data, indent=4))


def run_regular_expressions() -> None:
    regular_expressions(jewelry_html_1)
    regular_expressions(jewelry_html_2)


def run_xpath() -> None:
    xpath(jewelry_html_1)
    xpath(jewelry_html_2)


def run_road_runner() -> None:
    start_running(first_html=jewelry_html_1, second_html=jewelry_html_2)
