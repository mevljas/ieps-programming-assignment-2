from road_runner.helpers.constants import TOKEN_TYPE


class Token:
    def __init__(self, token_type: TOKEN_TYPE, value: str, real_tag: TOKEN_TYPE = None) -> None:
        self.token_type = token_type
        self.value = value
        self.real_tag = real_tag

    def __str__(self):
        return f'Type:{self.token_type}, value: {self.value}'

    def __repr__(self):
        return f'Type:{self.token_type}, value: {self.value}'
