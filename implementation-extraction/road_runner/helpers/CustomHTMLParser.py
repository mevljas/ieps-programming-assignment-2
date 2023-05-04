from html.parser import HTMLParser


class CustomHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.page_tokens = []

    def handle_starttag(self, tag, attrs):
        self.page_tokens.append(["initial_tag", tag])
        # print("< " + tag + " >")

    def handle_endtag(self, tag):
        self.page_tokens.append(["terminal_tag", tag])
        # print("</" + tag + " >")

    def handle_data(self, data):
        data = data.strip().lower()
        if data:
            self.page_tokens.append(["data", data])
        # print(data)

    def clear_page_tokens(self):
        self.page_tokens = []