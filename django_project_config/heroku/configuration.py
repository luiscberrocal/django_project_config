from pathlib import Path

from django_project_config.exceptions import DjangoProjectConfigException
from django_project_config.naming import VariableNaming
from django_project_config.utils import run_command, display_results


def create_heroku_app(app_name, **kwargs):
    """
    heroku apps:create {{ heroku_staging_app }}
    """
    verbose = kwargs.get('verbose', False)
    cwd = kwargs.get('run_folder')
    run_folder = kwargs.get('run_folder')
    command = f'heroku apps:create {app_name}'
    results, errors = run_command(command, cwd=cwd)
    if verbose:
        display_results(results, errors, title='CREATE HEROKU APP')


def create_postgresql_db(postgres_level, **kwargs):
    """
     heroku addons:create heroku-postgresql:hobby-dev
    """
    verbose = kwargs.get('verbose', False)
    cwd = kwargs.get('run_folder')
    command = f'heroku addons:create heroku-postgresql:{postgres_level}'
    results, errors = run_command(command, cwd=cwd)
    if verbose:
        display_results(results, errors, title='CREATE POSTGRES DATABASE')


def create_redis(redis_level, redis_name, **kwargs):
    """
    heroku addons:create heroku-redis:hobby-dev -a {{ django_project_slug | replace('_','-') }}-staging
    """
    verbose = kwargs.get('verbose', False)
    cwd = kwargs.get('run_folder')
    command = f'heroku addons:create heroku-redis:{redis_level} -a {redis_name}'
    results, errors = run_command(command, cwd=cwd)
    if verbose:
        display_results(results, errors, title='CREATE REDIS')


def run_heroku_config(**kwargs):
    heroku_slug = kwargs['base_slug']
    environment = kwargs['environment']
    verbose = kwargs['verbose']
    target_folder = kwargs['target_folder']
    run_folder = kwargs['run_folder']
    naming = VariableNaming(heroku_slug, environment, folder=target_folder)
    # STEP 01 Create heroku app
    if kwargs.get('create_heroku_app'):
        create_heroku_app(naming.heroku_app_name(), verbose=verbose, run_folder=run_folder )
    # STEP 02 Create database
    if kwargs.get('create_postgresql_db'):
        if environment == 'staging':
            level = 'hobby-dev'
        else:
            msg = f'Unsupported environment {environment}'
            raise DjangoProjectConfigException(msg)
        create_postgresql_db(level, verbose=verbose, run_folder=run_folder)
    # STEP 03 Create REDIS
    if kwargs.get('create_redis'):
        if environment == 'staging':
            level = 'hobby-dev'
        else:
            msg = f'Unsupported environment {environment}'
            raise DjangoProjectConfigException(msg)
        create_redis(level, naming.redis_name(), verbose=verbose, run_folder=run_folder)


if __name__ == '__main__':
    ROOT_FOLDER = Path(__file__).parent.parent.parent

    args = dict()
    args['verbose'] = True
    args['base_slug'] = 'home_auto_507_pty'
    args['environment'] = 'staging'
    args['target_folder'] = ROOT_FOLDER / 'output'
    args['create_heroku_app'] = False
    args['create_postgresql_db'] = False
    args['create_redis'] = True
    args['run_folder'] = ROOT_FOLDER
    print(f'>>>> {ROOT_FOLDER}')
    run_heroku_config(**args)
