from django_project_config.utils import run_command, Colors


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


def capture_input(*args, **kwargs):
    data = dict()
    data['base_slug'] = {'question': 'Heroku app base name', 'default': 'my-crazy-project'}
    data['environment'] = {'question': 'Environment', 'default': 'staging', 'choices': ['production', 'staging']}
    data['target_folder'] = {'question': 'Target folder', 'default': 'output'}
    data['create_heroku_app'] = {'question': 'Create Heroku app',
                                 'default': 'Y', 'choices': ['y', 'n']}

    # data['create_heroku_app'] = False
    # data['create_postgresql_db'] = False
    # data['create_redis'] = False
    # data['set_aws_variables'] = False
    # data['set_secrets'] = False
    # data['create_celery_broker_url'] = False
    # data['other'] = True
    # data['bucket_name'] = 'home-automation-staging-bucket'
    # data['aws_access_file'] = ROOT_FOLDER / 'output/home-automation-staging-user-access.json'
    # data['run_folder'] = ROOT_FOLDER
    for k, question in data.items():
        if question.get('choices'):
            display_choices = [x for x in question['choices']]
            for i, choice in enumerate(display_choices):
                if choice.upper() == question['default'].upper():
                    display_choices[i] = f'{Colors.BOLD}{Colors.OKGREEN}{question["default"]}{Colors.ENDC}'
            choices = f'({", ".join(display_choices)})'
            msg = f"{question['question']} {choices}: "
        else:
            msg = f"{question['question']} ({question['default']}): "
        question['value'] = input(msg)
        if question['value'] == '':
            question['value'] = question['default']

    print(data)

# if __name__ == '__main__':
#    app_name = 'home-auto-507-pty-staging'
#    h_vars = get_variables(app_name)
#    print(h_vars)
#
