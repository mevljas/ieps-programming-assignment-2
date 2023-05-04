from road_runner.helpers.CustomHTMLParser import CustomHTMLParser


def tokenize(page: str, html_parser: CustomHTMLParser) -> [str]:
    """
    Generate tokens from the HTML page using html_parser.
    :param html_parser: CustomHTMLParser object.
    :param page: HTML page string.
    :return: a list of tokens.
    """
    html_parser.feed(page)
    return html_parser.tokens


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
