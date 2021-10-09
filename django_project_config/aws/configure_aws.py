import subprocess
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

from django_project_config.naming import VariableNaming
from django_project_config.templating import template_helper
from django_project_config.utils import run_command, display_results, print_title


def run_piped_commands(command, encoding='utf-8'):
    command_parts = command.split('|')
    subprocesses = list()
    for i, c in enumerate(command_parts):
        if len(subprocesses) > 0:
            stdin = subprocess[i - 1]
        else:
            stdin = subprocess.PIPE
        commands = c.split(' ')
        result = subprocess.run(commands,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=stdin)
        subprocesses.append(result)
    result_lines = subprocesses[:-1].stdout.decode(encoding).split('\n')[:-1]
    error_lines = subprocesses[:-1].stderr.decode(encoding).split('\n')[:-1]
    return result_lines, error_lines


def get_buckets(bucket_name=None):
    command = f'aws s3 ls'  # | grep "{bucket_name}"'
    results, errors = run_command(command)
    if bucket_name is not None:
        results = [x for x in results if bucket_name in x]
    display_results(results, errors)


def create_bucket(bucket_name, **kwargs):
    verbose = kwargs.get('verbose', False)
    command = f'aws s3 mb s3://{bucket_name}'
    results, errors = run_command(command)
    if verbose:
        display_results(results, errors, title='CREATE BUCKET')
    return bucket_name


def create_aws_group(group_name, **kwargs):
    """aws iam create-group --group-name {{ aws_staging_group }}"""
    verbose = kwargs.get('verbose', False)
    commands = f'aws iam create-group --group-name {group_name}'
    results, errors = run_command(commands)
    if verbose:
        display_results(results, errors, title='CREATE AWS GROUP')
    return group


def create_policy_file(filename, bucket_name, **kwargs):
    verbose = kwargs.get('verbose', False)
    env = Environment(
        loader=PackageLoader("django_project_config"),
        autoescape=select_autoescape()
    )

    template = env.get_template("s3_policy.json.j2")
    content = template.render(aws_staging_bucket=bucket_name)
    if verbose:
        print_title('CREATE POLICY FILE')
        print(content)
    with open(filename, 'w') as json_file:
        json_file.write(content)
    return content


def create_policy(filename, bucket_name, **kwargs):
    """
   "aws iam create-policy --policy-name {{ aws_staging_bucket }}-policy --policy-document file://./output/{{ aws_staging_bucket }}_policy.json"
    :return: 
    """
    verbose = kwargs.get('verbose', False)
    commands = f"aws iam create-policy --policy-name {bucket_name}-policy" \
               f" --policy-document file://{filename}"
    results, errors = run_command(commands)
    if verbose:
        display_results(results, errors, title='CREATE POLICY')


def get_policy_arn(bucket_name, **kwargs):
    """
    aws iam list-policies --query
    'Policies[?PolicyName==`{{ aws_staging_bucket }}-policy`].{ARN:Arn}' --output text
    """
    verbose = kwargs.get('verbose', False)
    commands = f"aws iam list-policies --query " \
               f"'Policies[?PolicyName==`{bucket_name}-policy`].{{ARN:Arn}}' " \
               f"--output text"
    results, errors = run_command(commands)
    if verbose:
        display_results(results, errors)


def create_policy_arn_script(filename, bucket_name, aws_group, **kwargs):
    verbose = kwargs.get('verbose', False)

    template_name = 'grant_s3.sh.j2'
    template_data = {'bucket_name': bucket_name, "aws_group": aws_group}
    template_helper.write(filename, template_name, **kwargs)
    if verbose:
        content = template_helper.render(template_name, **template_data)
        print(content)


def execute_arn_script(filename, **kwargs):
    verbose = kwargs.get('verbose', False)
    commands = f'sh {filename}'
    results, errors = run_command(commands)
    if verbose:
        display_results(results, errors)


def create_user(username, **kwargs):
    """
    "aws iam create-user --user-name {{ aws_staging_user }}"
    :param username:
    :return:
    """
    verbose = kwargs.get('verbose', False)
    commands = f"aws iam create-user --user-name {username}"
    results, errors = run_command(commands)
    if verbose:
        display_results(results, errors)


def create_access_key(username, filename, **kwargs):
    """
    "aws iam create-access-key --user-name {{ aws_staging_user }} --output json > ./output/{{ aws_staging_user }}-access.json"
    :param filename:
    :param username:
    :param kwargs:
    :return:
    """
    verbose = kwargs.get('verbose', False)
    commands = f"aws iam create-access-key --user-name {username} " \
               f"--output json"
    results, errors = run_command(commands)
    if verbose:
        display_results(results, errors)
    with open(filename, 'w') as txt_file:
        txt_file.write(results)


def add_user_to_group(username, aws_group, **kwargs):
    """
 "aws iam add-user-to-group --user-name {{ aws_staging_user }} --group-name {{ aws_staging_group }}"
    :return:
    """
    verbose = kwargs.get('verbose', False)
    commands = f"aws iam add-user-to-group --user-name {username} " \
               f"--group-name {aws_group}"
    results, errors = run_command(commands)
    if verbose:
        display_results(results, errors, title='ADD USER TO GROUP')


if __name__ == '__main__':
    slug = 'home_automation'
    environment = 'staging'
    ROOT_FOLDER = Path(__file__).parent.parent.parent
    print(f'>>> {ROOT_FOLDER}')
    target_folder = ROOT_FOLDER / 'output'
    naming = VariableNaming(slug, environment, folder=target_folder)
    bucket = naming.bucket_name()
    group = naming.group()
    # STEP 01 Create Bucket
    if 1 == 0:
        create_bucket(bucket, verbose=True)
    # STEP 02 Create AWS buckets
    if 1 == 0:
        create_aws_group(group, verbose=True)

    # STEP 03 Create bucket policy
    if 1 == 0:
        create_policy_file(naming.policy_filename(), bucket, verbose=True)
        create_policy(naming.policy_filename(), bucket, verbose=True)
    # STEP 04 Create an assing arn policy
    if 1 == 1:
        create_policy_arn_script(naming.arn_script_filename(), bucket, group, verbose=True)
        execute_arn_script(naming.arn_script_filename(), verbose=True)

    # create_policy_arn_script(script_filename, bucket_name, aws_group)
    # execute_arn_script(script_filename, verbose=True)
    aws_username = 'home-automation-staging-user'
    # create_user(aws_username, verbose=True)

    access_filename = f'../output/{aws_username}-access.json'
    # create_access_key(aws_username, access_filename, verbose=True)
    # add_user_to_group(aws_username, aws_group, verbose=True)
