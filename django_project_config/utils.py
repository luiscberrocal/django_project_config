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


def print_title(title, sep='-', length=80):
    len_title = len(title) + 2
    deco = sep * int((len_title - length) / 2)
    display = f'{deco} {title} {deco}'
    return display[:length]


def display_results(results, errors, **kwargs):
    title = kwargs.get('title', 'Results')
    print_title(title, '-')
    for i, result in enumerate(results):
        print(f'{i + 1} {result}')
    print('-' * 80)
    print(errors)
