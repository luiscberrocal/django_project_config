from pathlib import Path

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


def run_main(**kwargs):
    project_slug = kwargs['project_slug']
    environment = kwargs['environment']
    verbose = kwargs['verbose']
    target_folder = kwargs['target_folder']
    naming = VariableNaming(project_slug, environment, folder=target_folder)
    # STEP 01 Create heroku app
    if kwargs.get('create_heroku_app'):
        create_heroku_app(naming.heroku_app_name(), verbose=verbose)


if __name__ == '__main__':
    ROOT_FOLDER = Path(__file__).parent.parent.parent

    args = dict()
    args['verbose'] = True
    args['project_slug'] = 'home_automation'
    args['environment'] = 'staging'
    args['target_folder'] = ROOT_FOLDER / 'output'
    args['create_heroku_app'] = True
    run_main(**args)
