from road_runner.helpers.CustomHTMLParser import CustomHTMLParser
from road_runner.helpers.constants import TOKEN_TYPE


def tokenize(page: str, html_parser: CustomHTMLParser) -> [str]:
    """
    Generate tokens from the HTML page using html_parser.
    :param html_parser: CustomHTMLParser object.
    :param page: HTML page string.
    :return: a list of tokens.
    """
    html_parser.feed(page)
    return html_parser.tokens


def get_printable_wrapper(wrapper: [str], new_line: str = '\n') -> str:
    """
    Generate printable string presentation of the wrapper.
    :param new_line: new line character which can be overridden to not print new lines.
    :param wrapper: roadrunner generated wrapper.
    :return: printable string presentation of the wrapper.
    """
    buffer = ""

    for token in wrapper:
        if token[0] == TOKEN_TYPE.OPENING_TAG:
            buffer += "".join(["<", token[1], f'>{new_line}'])
        elif token[0] == TOKEN_TYPE.CLOSING_TAG:
            buffer += "".join(["</", token[1], f'>{new_line}'])
        elif token[0] == TOKEN_TYPE.OPTIONAL:
            buffer += token[1] + new_line
        elif token[0] == TOKEN_TYPE.ITERATOR:
            buffer += "( " + get_printable_wrapper(wrapper=token[1], new_line='') + f' )+{new_line}'
        else:
            buffer += token[1] + new_line

    return buffer


def prepare_data(first_html: str, second_html: str) -> ([str], [str]):
    """
    Prepares the input data for the roadrunner algorithm.
    :param first_html: HTML of the first page.
    :param second_html: HTML of the second page.
    :return: first and second page tokens.
    """

    # Create HTML parser.
    html_parser = CustomHTMLParser()

    # Generate tokens from HTML.
    first_page_tokens = tokenize(page=first_html, html_parser=html_parser)
    html_parser.reset_parser()
    second_page_tokens = tokenize(page=second_html, html_parser=html_parser)

    return first_page_tokens, second_page_tokens
