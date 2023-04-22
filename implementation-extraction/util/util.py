def read_file(path: str, encoding: str) -> str:
    with open(path, encoding=encoding) as f:
        return f.read()