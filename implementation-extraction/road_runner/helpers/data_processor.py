from typing import Any

from bs4 import BeautifulSoup, Comment

from road_runner.constants import IGNORED_TAGS, IGNORED_TOKENS, HTML_TAG_START


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
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    # Remove comments.
    [comment.extract() for comment in comments]
    return soup


def clean_tokens(tokens: [str]) -> [str]:
    """
    Removes unnecessary tokens.
    :param tokens: a list of tokens.
    :return: filtered list of tokens.
    """
    return list(filter(lambda token: token not in IGNORED_TOKENS, tokens))


def generate_tokens(html_element: any) -> [str]:
    """
    Generate tokens from BeautifulSoup HTML elements.
    :param html_element: beautifulSoup HTML element.
    :return: a list of tokens.
    """
    tokens = [f'<{html_element.name}>']
    for child in html_element.contents:
        if not isinstance(child, str):
            tokens.extend(generate_tokens(html_element=child))
        else:
            tokens.extend(child.split())
    tokens.append(f'</{html_element.name}>')
    return tokens


def group_elements(tokens: [str]) -> [str]:
    """
    Group elements between the opening and closing HTML tags.
    :param tokens: a list of tokens.
    :return: a list of grouped tokens.
    """
    grouped_tokens = []
    window_start = 0
    while window_start < len(tokens):
        if tokens[window_start][0] != HTML_TAG_START:
            # Token is a data item or a closing HTML tag.
            window_end = window_start
            # Find the closing html tag.
            while tokens[window_end][0] != HTML_TAG_START:
                # While the end of the windows is not the closing tag.
                window_end = window_end + 1
            # The closing HTML tag was found.
            # Concatenate all items between the opening and closing HTML data.
            grouped_tokens.append(" ".join(tokens[window_start:window_end]))
            window_start = window_end
        else:
            # Append the opening HTML tag.
            grouped_tokens.append(tokens[window_start])
            window_start = window_start + 1
    return grouped_tokens


def prepare_data(first_html: str, second_html: str) -> tuple[Any, Any]:
    """
    Prepare the input data for the roadrunner algorithm.
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

    # Generate tokens from HTML tags and items.
    first_page_tokens = generate_tokens(html_element=first_soup.body)
    second_page_tokens = generate_tokens(html_element=second_soup.body)

    # Clean tokens.
    first_page_tokens = clean_tokens(tokens=first_page_tokens)
    second_page_tokens = clean_tokens(tokens=second_page_tokens)

    # Group elements between the opening and closing HTML tags.
    first_page_tokens = group_elements(tokens=first_page_tokens)
    second_page_tokens = group_elements(tokens=second_page_tokens)

    return first_page_tokens, second_page_tokens
