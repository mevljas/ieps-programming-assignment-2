def read_file(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()