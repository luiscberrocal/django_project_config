import subprocess

from jinja2 import Environment, PackageLoader, select_autoescape

from ..utils import run_command, display_results


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


def create_aws_group(group, **kwargs):
    """aws iam create-group --group-name {{ aws_staging_group }}"""
    verbose = kwargs.get('verbose', False)
    commands = f'aws iam create-group --group-name {group}'
    results, errors = run_command(commands)
    if verbose:
        display_results(results, errors, title='CREATE AWS GROUP')
    return group


def create_policy_file(filename, bucket_name, **kwargs):
    verbose = kwargs.get('verbose', False)
    env = Environment(
        loader=PackageLoader("scripts"),
        autoescape=select_autoescape()
    )

    template = env.get_template("s3_policy.json.j2")
    content = template.render(aws_staging_bucket=bucket_name)
    if verbose:
        print(content)
    with open(filename, 'w') as json_file:
        json_file.write(content)
    return content


def create_policy_file(filename, bucket_name, **kwargs):
    """
   "aws iam create-policy --policy-name {{ aws_staging_bucket }}-policy --policy-document file://./output/{{ aws_staging_bucket }}_policy.json"
    :return: 
    """
    verbose = kwargs.get('verbose', False)
    commands = f"aws iam create-policy --policy-name {bucket_name}-policy" \
               f" --policy-document file://{filename}"
    results, errors = run_command(commands)
    if verbose:
        display_results(results, errors)


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
    env = Environment(
        loader=PackageLoader("scripts"),
        autoescape=select_autoescape()
    )

    template = env.get_template("grant_s3.sh.j2")
    content = template.render(bucket_name=bucket_name, aws_group=aws_group)
    if verbose:
        print(content)
    with open(filename, 'w') as json_file:
        json_file.write(content)
    return content


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
    # create_bucket(project_slug=slug, dry_run=True)
    bucket_pattern = slug.replace('_', '-')
    # get_buckets(bucket_pattern)
    # group_name = create_aws_group(slug, verbose=True)
    bucket_name = f"{slug.replace('_', '-')}-staging-bucket"
    policy_filename = f'../output/{bucket_name}-s3-policy.json'
    # create_policy_file(policy_filename, bucket_name)
    # create_policy(bucket_name, policy_filename, verbose=True)
    aws_group = 'home-automation-staging-group'

    script_filename = f'../output/{bucket_name}-arn.sh'
    # create_policy_arn_script(script_filename, bucket_name, aws_group)

    # execute_arn_script(script_filename, verbose=True)
    aws_username = 'home-automation-staging-user'
    # create_user(aws_username, verbose=True)

    access_filename = f'../output/{aws_username}-access.json'
    # create_access_key(aws_username, access_filename, verbose=True)
    add_user_to_group(aws_username, aws_group, verbose=True)
