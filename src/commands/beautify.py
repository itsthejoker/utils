import string


def flip_char(char: str):
    if char in string.ascii_lowercase:
        return string.ascii_uppercase[string.ascii_lowercase.find(char)]
    else:
        return string.ascii_lowercase[string.ascii_uppercase.find(char)]


def main(args: list[str]):
    message = " ".join(args)
    new_beautiful_string = []

    for num, letter in enumerate(message):
        if letter in string.ascii_letters:
            if num % 2:
                new_beautiful_string.append(flip_char(letter))
                continue
        new_beautiful_string.append(letter)

    print("".join(new_beautiful_string))
