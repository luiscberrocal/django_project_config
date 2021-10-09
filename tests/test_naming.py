from django_project_config.naming import VariableNaming


def test_naming():
    project_slug = 'my_cool_project'
    environment = 'staging'
    naming = VariableNaming(project_slug, environment)
    assert naming.username() == 'my-cool-project-staging-user'
    assert naming.group() == 'my-cool-project-staging-group'
    assert naming.bucket_name() == 'my-cool-project-staging-bucket'

    assert naming.access_filename() == 'my-cool-project-staging-user-access.json'
    assert naming.policy_filename() == 'my-cool-project-staging-s3-policy.json'
    assert naming.arn_script_filename() == 'my-cool-project-staging-arn.sh'
