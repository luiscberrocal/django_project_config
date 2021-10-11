import hashlib
import json
from pathlib import Path
from time import time

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


def set_aws_variables(bucket_name, app_name, access_source_file, **kwargs):
    """
    "heroku config:set DJANGO_AWS_ACCESS_KEY_ID={{ access_keys.AccessKey.AccessKeyId }} --app {{heroku_staging_app}} "
    """
    verbose = kwargs.get('verbose', False)
    cwd = kwargs.get('run_folder')
    with open(access_source_file, 'r') as json_file:
        access_data = json.load(json_file)
    django_variables = dict()
    django_variables['DJANGO_AWS_ACCESS_KEY_ID'] = access_data['AccessKey']['AccessKeyId']
    django_variables['DJANGO_AWS_SECRET_ACCESS_KEY'] = access_data['AccessKey']['SecretAccessKey']
    django_variables['DJANGO_AWS_STORAGE_BUCKET_NAME'] = bucket_name
    set_heroku_variables(django_variables, app_name, cwd, verbose)


def set_heroku_variables(django_variables, app_name, cwd, verbose):
    for key, item in django_variables.items():
        command = f"heroku config:set {key}={item} --app {app_name}"
        results, errors = run_command(command, cwd=cwd)
        if verbose:
            display_results(results, errors, title=f'CREATE {key} for {app_name}')


def set_secrets(app_name, admin_url=None, **kwargs):
    cwd = kwargs.get('run_folder')
    verbose = kwargs.get('verbose', False)
    seed = kwargs.get('seed', str(time()))
    admin_len = kwargs.get('admin_len', 16)
    hashing = hashlib.sha1()
    hashing.update(f'{seed}'.encode('utf-8'))

    django_variables = dict()
    django_variables['DJANGO_SECRET_KEY'] = hashing.hexdigest()
    if admin_url is None:
        hashing.update(seed.encode('utf-8'))
        django_variables['DJANGO_ADMIN_URL'] = hashing.hexdigest()[:admin_len]
    set_heroku_variables(django_variables, app_name, cwd, verbose)


def run_heroku_config(**kwargs):
    heroku_slug = kwargs['base_slug']
    environment = kwargs['environment']
    verbose = kwargs['verbose']
    target_folder = kwargs['target_folder']
    run_folder = kwargs['run_folder']
    naming = VariableNaming(heroku_slug, environment, folder=target_folder)
    # STEP 01 Create heroku app
    if kwargs.get('create_heroku_app'):
        create_heroku_app(naming.heroku_app_name(), verbose=verbose, run_folder=run_folder)
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
    # STEP 04 Create AWS variables.
    if kwargs.get('set_aws_variables'):
        set_aws_variables(kwargs['bucket_name'], naming.heroku_app_name(), kwargs['aws_access_file'],
                          verbose=verbose, run_folder=run_folder)
    # STEP 05 Create secrets and admin url
    if kwargs.get('set_secrets'):
        set_secrets(naming.heroku_app_name(), verbose=verbose)


if __name__ == '__main__':
    ROOT_FOLDER = Path(__file__).parent.parent.parent

    args = dict()
    args['verbose'] = True
    args['base_slug'] = 'home_auto_507_pty'
    args['environment'] = 'staging'
    args['target_folder'] = ROOT_FOLDER / 'output'
    args['create_heroku_app'] = False
    args['create_postgresql_db'] = False
    args['create_redis'] = False
    args['set_aws_variables'] = False
    args['set_secrets'] = True
    args['bucket_name'] = 'home-automation-staging-bucket'
    args['aws_access_file'] = ROOT_FOLDER / 'output/home-automation-staging-user-access.json'

    args['run_folder'] = ROOT_FOLDER
    print(f'>>>> {ROOT_FOLDER}')
    run_heroku_config(**args)
