def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()