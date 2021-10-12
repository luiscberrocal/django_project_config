from django_project_config.utils import run_command


def get_variables(app_name, **kwargs):
    """
    heroku config --app {{heroku_staging_app}}
    """
    verbose = kwargs.get('verbose', False)
    command = f'heroku config --app {app_name}'
    results, errors = run_command(command)
    heroku_vars = dict()
    for result in results:
        if ':' in result:
            splits = result.split(':')
            heroku_vars[splits[0]] = (':'.join(splits[1:])).strip()
    return heroku_vars

#if __name__ == '__main__':
#    app_name = 'home-auto-507-pty-staging'
#    h_vars = get_variables(app_name)
#    print(h_vars)
#
