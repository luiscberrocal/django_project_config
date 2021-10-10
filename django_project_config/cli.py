"""Console script for django_project_config."""
import argparse
import sys
from pathlib import Path

from django_project_config.heroku.configuration import run_heroku_config


def main():
    """Console script for django_project_config."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "django_project_config.cli.main")
    ROOT_FOLDER = Path(__file__).parent.parent.parent
    print(f'>>> Root: {ROOT_FOLDER}')
    args = dict()
    args['verbose'] = True
    args['base_slug'] = 'home_auto_507_pty'
    args['environment'] = 'staging'
    args['target_folder'] = ROOT_FOLDER / 'output'
    args['create_heroku_app'] = False
    args['create_postgresql_db'] = True
    run_heroku_config(**args)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
