import re
import json

from util.util import read_file

jewelry_html_1 = read_file("../input-extraction/overstock.com/jewelry01.html")
jewelry_html_2 = read_file("../input-extraction/overstock.com/jewelry02.html")


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
    content_regex = r'<span class="normal">([\S\s]*?)</span>'
    contents = re.findall(content_regex, html)
    # remove everything after <br tag (anchor tags, spans, etc.) and replace newlines inside the text
    contents = [content.split("<br")[0].replace("\n", " ").strip() for content in contents]

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
            "Content": contents[i]
        })

    # output JSON 
    print(json.dumps(data, indent=4))

def run_regular_expressions() -> None:
    print("Running regular expressions for first page...")
    regular_expressions(jewelry_html_1)
    print("Running regular expressions for second page...")
    regular_expressions(jewelry_html_2)
    print("Done.")