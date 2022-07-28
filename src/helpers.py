import string


def flip_char(char: str):
    if char in string.ascii_lowercase:
        return string.ascii_uppercase[string.ascii_lowercase.find(char)]
    else:
        return string.ascii_lowercase[string.ascii_uppercase.find(char)]
