"""Console script for django_project_config."""
import argparse
import sys

from django_project_config.heroku.utils import capture_input


def main():
    # Create the parser
    my_parser = argparse.ArgumentParser(description='Configure Django project')

    # Add the arguments
    my_parser.add_argument('command', metavar='command', type=str, help='Command')
    my_parser.add_argument('component', metavar='component', type=str,
                           help='Compponent to apply the comand to')

    # Execute the parse_args() method
    args = my_parser.parse_args()
    print(f'>>> {args.command} {args.component}')
    if args.command == 'config' and args.component == 'heroku':
        capture_input()

if __name__ == "__main__":
    """
    django_project_config config heroku --app heroku-app-name --env staging 
    """
    sys.exit(main())  # pragma: no cover
