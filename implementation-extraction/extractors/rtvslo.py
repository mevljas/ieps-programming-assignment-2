import re
import json

from bs4 import BeautifulSoup
from lxml import etree
from extractors.helpers.helper import read_file, prettify_text
from road_runner.road_runner import start_running

# on macOS, the following encoding is needed to read the files: "utf-8"
audi_html = read_file("../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html", "utf-8")
volvo_html = read_file("../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html", "utf-8")

def regular_expressions(html) -> None:
    # Author
    author_regex = r'<div class="author-name">(.*?)</div>'
    author = re.findall(author_regex, html)[0]

    # Published time
    published_time_regex = r'<div class="publish-meta">[\n\s\t]*(.*?)<br>'
    published_time = re.findall(published_time_regex, html)[0]
    
    # Title
    title_regex = r'<h1>(.*?)</h1>'
    title = re.findall(title_regex, html)[0]

    # Subtitle
    subtitle_regex = r'<div class="subtitle">(.*?)</div>'
    subtitle = re.findall(subtitle_regex, html)[0]

    # Lead
    lead_regex = r'<p class="lead">(.*?)</p>'
    lead = re.findall(lead_regex, html)[0]

    # Content
    content_regex = r'^(?:.*)<div class="article-body">|<div class="gallery">(?:.*)$|<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>|<[^>]*>'
    content = re.sub(content_regex, '', html, flags=re.S)
    content = prettify_text(content)

    # output JSON
    data = {
        "Author": author,
        "PublishedTime": published_time,
        "Title": title,
        "Subtitle": subtitle,
        "Lead": lead,
        "Content": content
    }
    print(json.dumps(data, indent=4, ensure_ascii=False))

def xpath(html) -> None:
    soup = BeautifulSoup(html, 'html.parser')
    dom = etree.HTML(str(soup))

    # Author
    author = dom.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[1]/div')[0].text

    # Published time
    published_time = dom.xpath('//*[@id="main-container"]/div[3]/div/div[1]/div[2]/text()[1]')[0].strip()

    # Title
    title = dom.xpath('//*[@id="main-container"]/div[3]/div/header/h1')[0].text

    # Subtitle
    subtitle = dom.xpath('//*[@id="main-container"]/div[3]/div/header/div[2]')[0].text
    
    # Lead
    lead = dom.xpath('//*[@id="main-container"]/div[3]/div/header/p')[0].text
    
    # Content
    # select the root of the content element
    content_root = dom.xpath('//*[@id="main-container"]/div[3]/div/div[2]')[0]

    # ignore script tags
    content_elements = content_root.xpath('./descendant::*[not(name() = "script")]/text()')
    ## TODO: failed variations to ignore the gallery div!
    # content_elements = content_root.xpath('.//*[not(descendant-or-self::div[@class="gallery"]) and not(self::script)]')
    # content_elements = content_root.xpath('.//*[not(contains(@class, "gallery")) and not(self::script)]/text()')
    # content_elements = content_root.xpath('//*[not(.//article/div)]/text()')
    # content_elements = content_root.xpath('.//*[not(descendant::article//div[@class="gallery"])]/text()')

    # join the text strings and remove leading/trailing whitespace
    content_text = ''.join(content_elements).strip()

    # remove empty lines
    article_lines = content_text.split('\n')
    article_text = '\n'.join(line.strip() for line in article_lines if line.strip())

    # output JSON
    data = {
        "Author": author,
        "PublishedTime": published_time,
        "Title": title,
        "Subtitle": subtitle,
        "Lead": lead,
        "Content": article_text
    }
    print(json.dumps(data, indent=4, ensure_ascii=False))

def run_regular_expressions() -> None:
    regular_expressions(audi_html)
    regular_expressions(volvo_html)

def run_xpath() -> None:
    xpath(audi_html)
    xpath(volvo_html)

def run_road_runner() -> None:
    start_running(first_html=audi_html, second_html=volvo_html)