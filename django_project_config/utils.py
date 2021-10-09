import subprocess


def run_command(command, encoding='utf-8', eol='\n'):
    commands = command.split(' ')
    result = subprocess.run(commands,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    result_lines = result.stdout.decode(encoding).split(eol)[:-1]
    error_lines = result.stderr.decode(encoding).split(eol)[:-1]
    return result_lines, error_lines


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'  # Yellow
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_title(title, sep='-', length=80):
    len_title = len(title) + 2
    deco = sep * int((length - len_title) / 2)
    display = f'{deco} {title} {deco}'
    print(display[:length])


def print_line(sep='-', length=80, **kwargs):
    color = kwargs.get('color')
    if color is None:
        print(sep * length)
    else:
        print(f'{color}{sep}{Colors.ENDC}' * length)


def display_results(results, errors, **kwargs):
    title = kwargs.get('title', 'Results')
    length = kwargs.get('length', 80)
    sep = kwargs.get('sep', '-')
    print_title(title, sep, length=length)
    for i, result in enumerate(results):
        print(f'{i + 1} {result}')
    print(sep * length)
    if len(errors) > 0:
        print(f'{Colors.WARNING}-{Colors.ENDC}' * length)
        for i, error in enumerate(errors):
            print(f'{i + 1} {error}')

