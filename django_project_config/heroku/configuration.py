from pathlib import Path

from django_project_config.exceptions import DjangoProjectConfigException
from django_project_config.naming import VariableNaming
from django_project_config.utils import run_command, display_results


def create_heroku_app(app_name, **kwargs):
    """
    heroku apps:create {{ heroku_staging_app }}
    """
    verbose = kwargs.get('verbose', False)
    command = f'heroku apps:create {app_name}'
    results, errors = run_command(command)
    if verbose:
        display_results(results, errors, title='CREATE HEROKU APP')


def create_postgresql_db(postgres_level, **kwargs):
    """
     heroku addons:create heroku-postgresql:hobby-dev
    """
    verbose = kwargs.get('verbose', False)
    command = f'heroku apps:create heroku-postgresql:{postgres_level}'
    results, errors = run_command(command)
    if verbose:
        display_results(results, errors, title='CREATE POSTGRES DATABASE')


def run_heroku_config(**kwargs):
    heroku_slug = kwargs['base_slug']
    environment = kwargs['environment']
    verbose = kwargs['verbose']
    target_folder = kwargs['target_folder']
    naming = VariableNaming(heroku_slug, environment, folder=target_folder)
    # STEP 01 Create heroku app
    if kwargs.get('create_heroku_app'):
        create_heroku_app(naming.heroku_app_name(), verbose=verbose)
    # STEP 02 Create database
    if kwargs.get('create_postgresql_db'):
        if environment == 'staging':
            level = 'hobby-dev'
        else:
            msg = f'Unsupported environment {environment}'
            raise DjangoProjectConfigException(msg)
        create_postgresql_db(level, verbose=verbose)


if __name__ == '__main__':
    ROOT_FOLDER = Path(__file__).parent.parent.parent

    args = dict()
    args['verbose'] = True
    args['base_slug'] = 'home_auto_507_pty'
    args['environment'] = 'staging'
    args['target_folder'] = ROOT_FOLDER / 'output'
    args['create_heroku_app'] = False
    args['create_postgresql_db'] = True

    run_heroku_config(**args)
