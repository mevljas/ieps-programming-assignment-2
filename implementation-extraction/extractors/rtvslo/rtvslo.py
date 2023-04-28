import re
import json

from bs4 import BeautifulSoup
from util.util import read_file

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
    content_regex = r'<div class="article-body">(.*?)<div class="gallery">'
    content = re.findall(content_regex, html, re.S)[0]

    soup = BeautifulSoup(content, 'html.parser')
    article_text = soup.get_text(separator='\n\n').strip()
    article_lines = article_text.split('\n')
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
    print("Running regular expressions for first page...")
    regular_expressions(audi_html)
    print("Running regular expressions for second page...")
    regular_expressions(volvo_html)
    print("Done.")