def read_MosAPIKey(filepath: str) -> str:
    with open(filepath, 'r') as API_file:
        API_KEY = API_file.read()
    return API_KEY