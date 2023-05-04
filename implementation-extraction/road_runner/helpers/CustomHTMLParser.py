from html.parser import HTMLParser

from road_runner.helpers.constants import TOKEN_TYPE


class CustomHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.tokens = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """
        Handler for HTML opening tags.
        :param tag: HTML tag.
        :param attrs: tag attributes.
        """
        self.tokens.append([TOKEN_TYPE.OPENING_TAG, tag])

    def handle_endtag(self, tag: str) -> None:
        """
        Handler for HTML closing tags.
        :param tag: HTML tag.
        """
        self.tokens.append([TOKEN_TYPE.CLOSING_TAG, tag])

    def handle_data(self, data: str) -> None:
        """
        Handler for HTML data.
        :param data: HTML data.
        """
        data = data.strip()
        if data:
            self.tokens.append(["database_field", data])

    def reset_parser(self) -> None:
        """
        Helper method to reset the list of tokens.
        """
        self.tokens = []
