from html.parser import HTMLParser

from road_runner.helpers.Token import Token
from road_runner.helpers.constants import TOKEN_TYPE


class CustomHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.tokens: [Token] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """
        Handler for HTML opening tags.
        :param tag: HTML tag.
        :param attrs: tag attributes.
        """
        self.tokens.append(Token(token_type=TOKEN_TYPE.OPENING_TAG, value=tag))

    def handle_endtag(self, tag: str) -> None:
        """
        Handler for HTML closing tags.
        :param tag: HTML tag.
        """
        self.tokens.append(Token(token_type=TOKEN_TYPE.CLOSING_TAG, value=tag))

    def handle_data(self, data: str) -> None:
        """
        Handler for HTML data.
        :param data: HTML data.
        """
        data = data.strip()
        if data:
            self.tokens.append(Token(token_type=TOKEN_TYPE.DATABASE_FIELD, value=data))

    def reset_parser(self) -> None:
        """
        Helper method to reset the list of tokens.
        """
        self.tokens: [Token] = []
