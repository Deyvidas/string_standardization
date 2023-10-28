import re


SINGLE_RIGHT_SPACE = '.,:;!?%'
SINGLE_LEFT_SPACE = '№'
SINGLE_CAPITALIZE = '.:;!?'
MIDDLE = '-&/`'
PAIR_LEFT = r'(\[\{«„‘'
PAIR_RIGHT = r')\]\}»“’'
ALL_CHARS = r'!\"#$%&()*+,-./:;>=<?@\[\]^_`|\{\}~\'\\«»„“‘’№'


def remove_extra_blank(string: str) -> str:
    """
    Remove extra spaces between signs, if more than 1 and if isn't after `\\n`.
    """
    lines = string.strip().split('\n')
    for i, line in enumerate(lines):
        line_head = re.findall(r'^[ ]{0,}', line)[0]
        line = line_head + ' '.join(line.strip().split())
        lines[i] = line
    return '\n'.join(lines)


def remove_space_around_punctuation(string: str) -> str:
    """
    Remove ONE right & left space around each character in `ALL_CHARS`.
    Take string with already cleared, where between chars max one space.
    """
    regex = f'[{ALL_CHARS}]'
    founded_chars = set(re.findall(regex, string))
    for char in founded_chars:
        string = string.replace(f' {char}', f'{char}')
        string = string.replace(f'{char} ', f'{char}')
    return string


def make_string_capitalized(string: str) -> str:
    """
    Set upper first character and chars which has more than one space between
    `SINGLE_CAPITALIZE`.
    Take string with already cleared, where between chars max one space.
    """
    if string == str():
        return string

    regex = rf'[{SINGLE_CAPITALIZE}][\W_]+[^\W\d_]'
    if string[0].isalpha():
        string = string[0].upper() + string[1:]

    substrings = set(re.findall(regex, string))
    for substring in substrings:
        capitalized_substring = substring[:-1] + substring[-1].upper()
        string = string.replace(substring, capitalized_substring)

    return string


def make_slice_capitalized(slice: str) -> str:
    """
    Make upper first word char after `SINGLE_CAPITALIZE` chars, and return
    slice with capitalized word char, length is not increased.
    """
    if len(slice) != 3:
        raise ValueError('function cant work with strings which length != 3.')

    if slice[1] not in SINGLE_CAPITALIZE:
        return slice

    slice = f'{slice[0]}{slice[1]}{slice[2].upper()}'
    return slice


def remove_space_between_digits_in_slice(slice: str) -> str:
    r"""
    Remove space between two digit for example `0 0` -> `00`, and return slice
    without space char, length is changed (-1) if slice has `[\d][ ][\d]`.
    """
    if len(slice) != 3:
        raise ValueError('function cant work with strings which length != 3.')

    regex = r'[\d][ ][\d]'
    found = re.findall(regex, slice)
    if found == list():
        return slice

    slice = f'{slice[0]}{slice[2]}'
    return slice


def add_left_space_to_slice(slice: str) -> str:
    """
    Add space between word character and open parentheses or char №, and return
    string which length incremented with 1 char.
    """
    if len(slice) != 3:
        raise ValueError('function cant work with strings which length != 3.')

    a = ALL_CHARS
    chars_with_left_space = PAIR_LEFT + SINGLE_LEFT_SPACE
    similar_regex = rf'[{a}][{chars_with_left_space}].'
    similar_found = re.findall(similar_regex, slice)
    if similar_found != list():
        return slice

    if slice[1] not in chars_with_left_space or slice[0] == ' ':
        return slice

    slice = f'{slice[0]} {slice[1]}{slice[2]}'
    return slice


def add_right_space_to_slice(slice: str) -> str:
    """
    Add space between close parentheses and word character, and return string
    which length incremented with 1 char.
    """
    if len(slice) != 3:
        raise ValueError('function cant work with strings which length != 3.')

    # To prevent insert space between:
    #     - similar chars !!, ..., !?, %-;
    #     - end of line and \n char;
    #     - digits dot separated 44.33.
    a = rf'{ALL_CHARS}\n'
    chars_with_right_space = PAIR_RIGHT + SINGLE_RIGHT_SPACE
    similar_regex = rf'.[{chars_with_right_space}][{a}]'
    digit_dot_sep_regex = r'[\d][.][\d]'
    similar_found = re.findall(similar_regex, slice)
    digit_sep_found = re.findall(digit_dot_sep_regex, slice)
    found = similar_found + digit_sep_found

    if slice[1] not in chars_with_right_space or found != list():
        return slice

    slice = f'{slice[0]}{slice[1]} {slice[2]}'
    return slice


def prepare_string(string: str) -> str:
    """
    Return cleared from extra-blank string and set upper first character and
    chars which has more than one space between `SINGLE_CAPITALIZE`.
    """
    string = remove_extra_blank(string)
    string = remove_space_around_punctuation(string)
    string = make_string_capitalized(string)
    return string


def clean_string(string: str) -> str:
    """Standardize string and return it."""
    string = prepare_string(string)
    slice_size = 3
    if len(string) < slice_size:
        return string

    functions = (
        make_slice_capitalized,
        remove_space_between_digits_in_slice,
        add_left_space_to_slice,
        add_right_space_to_slice,
    )
    flag, i = True, slice_size - 1
    while flag is True:
        slice = string[i - 2] + string[i - 1] + string[i]

        for function in functions:
            if len(slice) != 3:
                continue
            slice = function(slice)
            string = f'{string[:i - 2]}{slice}{string[i + 1:]}'

        i += 1
        flag = i < len(string)
    return string
