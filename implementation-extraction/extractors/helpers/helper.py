import re
from bs4 import BeautifulSoup

def read_file(path: str, encoding: str) -> str:
    with open(path, encoding=encoding) as f:
        return f.read()

def extract_text_from_html(html: str) -> str:
    ## Using a HTML parser
    # soup = BeautifulSoup(html, 'html.parser')
    # content_text = soup.get_text(separator='\n\n').strip()
    # content_lines = content_text.split('\n')
    # content_text = '\n'.join(line.strip() for line in content_lines if line.strip())
    # return content_text

    ## Using only regular expressions
    # remove script tags from content
    content = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', html)
    # substitute <br> tags with newlines
    content = re.sub(r'<br>', '\n', content)
    # insert newline at start of each paragraph
    content = re.sub(r'<p\b[^>]*>', '\n<p>', content)
    # extract text from content
    content = re.sub(r'<[^>]*>', '', content)
    # decode html whitespaces
    content = re.sub(r'&nbsp;', ' ', content)
    # remove leading and trailing whitespace and unnecessary newlines
    content_lines = content.split('\n')
    content_text = '\n'.join(line.strip() for line in content_lines if line.strip())
    
    return content_text

def prettify_text(html: str) -> str:
    # decode html whitespaces
    content = re.sub(r'&nbsp;', ' ', html)
    # remove leading and trailing whitespace and unnecessary newlines
    content_lines = content.split('\n')
    content_text = '\n'.join(line.strip() for line in content_lines if line.strip())
    
    return content_text