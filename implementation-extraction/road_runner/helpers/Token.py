from road_runner.helpers.constants import TOKEN_TYPE


class Token:
    def __init__(self, token_type: TOKEN_TYPE, value: str) -> None:
        self.token_type = token_type
        self.value = value
