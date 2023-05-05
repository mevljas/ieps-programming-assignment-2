from bs4 import BeautifulSoup, Comment

from road_runner.helpers.CustomHTMLParser import CustomHTMLParser
from road_runner.helpers.Token import Token
from road_runner.helpers.constants import TOKEN_TYPE, IGNORED_TAGS


def create_soup(html: str) -> BeautifulSoup:
    """
    Creates a BeautifulSoup object with the provided html.
    :param html: html data to be used.
    :return: generated BeautifulSoup object.
    """
    return BeautifulSoup(html, "html.parser")


def clean_html(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Removes unnecessary tags and comments from the HTML.
    :param soup: beautifulSoup object with html data to be cleaned.
    :return: beautifulSoup object with cleaned html data.
    """
    # Remove tags.
    [x.extract() for x in soup.findAll(IGNORED_TAGS)]
    # Find comments.
    comments = soup.findAll(string=lambda text: isinstance(text, Comment))
    # Remove comments.
    [comment.extract() for comment in comments]
    return soup


def tokenize(page: str, html_parser: CustomHTMLParser) -> [str]:
    """
    Generate tokens from the HTML page using html_parser.
    :param html_parser: CustomHTMLParser object.
    :param page: HTML page string.
    :return: a list of tokens.
    """
    html_parser.feed(page)
    return html_parser.tokens

def close_optional_tag(is_optional: bool, new_line: str = '\n') -> str:
    """
    Closes optional tag if it's currently open.
    :param is_optional: Determines whether the tag is currently open.
    :param new_line: Determines whether the text should end with a newline.
    :return: Text which will be added to the buffer.
    """
    return f")?{new_line}" if is_optional else ""

def get_printable_wrapper(wrapper: [Token], new_line: str = '\n') -> str:
    """
    Generate printable string presentation of the wrapper.
    :param new_line: new line character which can be overridden to not print new lines.
    :param wrapper: roadrunner generated wrapper.
    :return: printable string presentation of the wrapper.
    """
    buffer = ""
    is_optional: bool = False

    for token in wrapper:
        match token.token_type:
            case TOKEN_TYPE.OPENING_TAG:
                buffer += close_optional_tag(is_optional=is_optional, new_line=new_line)
                is_optional = False
                buffer += f"<{token.value}>{new_line}"
            case TOKEN_TYPE.CLOSING_TAG:
                buffer += close_optional_tag(is_optional=is_optional)
                is_optional = False
                buffer += f"</{token.value}>{new_line}"
            case TOKEN_TYPE.OPTIONAL:
                if not is_optional:
                    buffer += "("
                    is_optional = True
                if token.real_tag == TOKEN_TYPE.OPENING_TAG:
                    buffer += f"<{token.value}>"
                elif token.real_tag == TOKEN_TYPE.CLOSING_TAG:
                    buffer += f"<{token.value}/>"
                else:
                    buffer += token.value
            case TOKEN_TYPE.ITERATOR:
                buffer += close_optional_tag(is_optional=is_optional, new_line='')
                is_optional = False
                buffer += f"({get_printable_wrapper(wrapper=token.value, new_line='')})+{new_line}"
            case _:
                buffer += close_optional_tag(is_optional=is_optional)
                is_optional = False
                buffer += token.value + new_line



    return buffer


def prepare_data(first_html: str, second_html: str) -> ([Token], [Token]):
    """
    Prepares the input data for the roadrunner algorithm.
    :param first_html: HTML of the first page.
    :param second_html: HTML of the second page.
    :return: first and second page tokens.
    """

    # Create Beautiful soup objects.
    first_soup = create_soup(html=first_html)
    second_soup = create_soup(html=second_html)

    # Clean HTML.
    first_soup = clean_html(soup=first_soup)
    second_soup = clean_html(soup=second_soup)

    # Create HTML parser.
    html_parser = CustomHTMLParser()

    # Generate tokens from HTML.
    first_page_tokens = tokenize(page=first_soup.prettify(), html_parser=html_parser)
    html_parser.reset_parser()
    second_page_tokens = tokenize(page=second_soup.prettify(), html_parser=html_parser)

    return first_page_tokens, second_page_tokens
