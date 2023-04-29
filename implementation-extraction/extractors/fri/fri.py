import re
import json

from bs4 import BeautifulSoup
from lxml import etree
from util.util import read_file

# on macOS, the following encoding is needed to read the files: "utf-8"
student_devrev_html = read_file("../input-extraction/fri.uni-lj.si/Kako izbrati študentsko delo in kje pričeti profesionalno kariero (in zakaj bi to lahko bil DevRev)_.html", "utf-8")
info_dan_mag_html = read_file("../input-extraction/fri.uni-lj.si/Informativni dan za magistrski študij.html", "utf-8")

def regular_expressions(html) -> None:
    # Published date
    published_date_regex = r'<div class="text">[\n\s\S]*?<br>(.*?)[\n\s]*?<\/div>'
    published_date = re.findall(published_date_regex, html)[0]

    # Title
    title_regex = r'<div class="heading-article\snovica-title">[\n\s]*<ul>[\n\s]*<li\s.*?>(.*)<\/li>'
    title = re.findall(title_regex, html)[0].strip()

    # Category
    category_regex = r'<span class="kategorija">(.*?)<\/span>'
    category = re.findall(category_regex, html)[0]

    # Lead
    lead_regex = r'<p(?:\s+class="rtejustify")?>(?:<[^>]*>)*(.*?)(?:<\/[^>]*>)*<\/p'
    lead = re.findall(lead_regex, html)[0].strip()

    soup = BeautifulSoup(lead, 'html.parser')
    lead_text = soup.get_text(separator='\n\n').strip()
    lead_lines = lead_text.split('\n')
    lead_text = ' '.join(line.strip() for line in lead_lines if line.strip())

    # Content
    content_regex = r'<div class="novica-content">[\n\s\S]*?<br>[\n\s]*(.*?)<\/div>'
    content = re.findall(content_regex, html, re.S)[0]

    soup = BeautifulSoup(content, 'html.parser')
    article_text = soup.get_text(separator='\n\n').strip()
    article_lines = article_text.split('\n')
    article_text = ' '.join(line.strip() for line in article_lines if line.strip())

    # output JSON
    data = {
        "PublishedDate": published_date,
        "Title": title,
        "Category": category,
        "Lead": lead_text,
        "Content": article_text
    }
    print(json.dumps(data, indent=4, ensure_ascii=False))

def xpath(html) -> None:
    soup = BeautifulSoup(html, 'html.parser')
    dom = etree.HTML(str(soup))

    # Published date
    published_date = dom.xpath('//*[@id="banner-header"]/div[2]/div/div[3]/text()[2]')[0].strip()

    # Category
    category = dom.xpath('//*[@id="katedre-container"]/div[2]/span')[0].text
    
    # Title
    title = dom.xpath('//*[@id="katedre-container"]/div[1]/div[1]/ul/li')[0].text
    
    # Lead
    lead = dom.xpath('//*[@id="katedre-container"]/div[3]/p[1]/strong/span/span/span')
    if len(lead) == 0:
        lead = dom.xpath('//*[@id="katedre-container"]/div[3]/p[1]/strong')
    lead = lead[0].text

    # Content
    content_root = dom.xpath('//*[@id="katedre-container"]/div[3]/*[position() > 2]')
    # join all text nodes
    article_text = "\n".join([child.xpath('string()').strip() for child in content_root])
    # remove empty lines
    article_lines = article_text.split('\n')
    article_text = '\n'.join(line.strip() for line in article_lines if line.strip())

    # output JSON
    data = {
        "PublishedDate": published_date,
        "Category": category,
        "Title": title,
        "Lead": lead,
        "Content": article_text
    }
    print(json.dumps(data, indent=4, ensure_ascii=False))

def run_regular_expressions() -> None:
    print("Running regular expressions for first page...")
    regular_expressions(student_devrev_html)
    print("Running regular expressions for second page...")
    regular_expressions(info_dan_mag_html)
    print("Done.")

def run_xpath() -> None:
    print("Running XPath for first page...")
    xpath(student_devrev_html)
    print("Running XPath for second page...")
    xpath(info_dan_mag_html)
    print("Done.")