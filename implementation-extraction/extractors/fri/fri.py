import re
import json

from bs4 import BeautifulSoup
from lxml import etree
from util.util import read_file

# on macOS, the following encoding is needed to read the files: "utf-8"
pacman_ctf_html = read_file("../input-extraction/fri.uni-lj.si/Eutopia Pacman Capture the Flag.html", "utf-8")
nasa_dewesoft_html = read_file("../input-extraction/fri.uni-lj.si/Nasin povratek na Luno s pomočjo slovenskega podjetja Dewesoft.html", "utf-8")

def regular_expressions(html) -> None:
    # Published date
    published_date_regex = r'<div class="text">[\n\s\S]*?<br>(.*?)[\n\s]*?<\/div>'
    published_date = re.findall(published_date_regex, html)[0]

    # Title
    title_regex = r'<div class="heading-article\snovica-title">[\n\s]*<ul>[\n\s]*<li\s.*?>(.*)<\/li>'
    title = re.findall(title_regex, html)[0].strip()

    # Lead
    lead_regex = r'<p(?:\s+class="rtejustify")?>(?:<[^>]*>)*(.*?)(?:<\/[^>]*>)*<\/p'
    lead = re.findall(lead_regex, html)[0].strip()

    # Content
    content_regex = r'<div class="novica-content">[\n\s\S]*<br>[\n\s]*(.*?)<\/div>'
    content = re.findall(content_regex, html, re.S)[0]

    soup = BeautifulSoup(content, 'html.parser')
    article_text = soup.get_text(separator='\n\n').strip()
    article_lines = article_text.split('\n')
    article_text = '\n'.join(line.strip() for line in article_lines if line.strip())

    # output JSON
    data = {
        "PublishedDate": published_date,
        "Title": title,
        "Lead": lead,
        "Content": article_text
    }
    print(json.dumps(data, indent=4, ensure_ascii=False))

def xpath(html) -> None:
    # TODO: implement
    pass

def run_regular_expressions() -> None:
    print("Running regular expressions for first page...")
    regular_expressions(pacman_ctf_html)
    print("Running regular expressions for second page...")
    regular_expressions(nasa_dewesoft_html)
    print("Done.")

def run_xpath() -> None:
    print("Running XPath for first page...")
    xpath(pacman_ctf_html)
    print("Running XPath for second page...")
    xpath(nasa_dewesoft_html)
    print("Done.")