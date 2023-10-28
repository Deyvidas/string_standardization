from module.standardizes import clean_string


def generate_random_string():
    singles = r'!#$%&*+,-./:;>=<?@^_`|~\\№'
    pairs = (
        ('(', ')'),
        ('«', '»'),
        ('„', '“'),
        ('‘', '’'),
        ('"', '"'),
        ('[', ']'),
        ('{', '}'),
        ("'", "'"),
    )
    ready_string = str()
    for f in ['string', '000000']:
        for single in singles:
            ready_string += f'case for [{single}]:\n'
            ready_string += f'{f}  {single}  {f}  \n\n'
        for pair in pairs:
            ready_string += f'case for [{pair[0]} {pair[1]}]:\n'
            ready_string += f'{f}  {pair[0]}  {f}  {pair[1]}  {f}\n\n'
    return ready_string


string = generate_random_string()
clean = clean_string(string)


for i, pack in enumerate(zip(string.split('\n'), clean.split('\n'))):
    string = f'[{pack[0]}] -> [{pack[1]}]'
    if i % 3 == 0:
        string = f'{pack[1]}'
    if pack[0] == '':
        string = '-' * 79
    print(string)
