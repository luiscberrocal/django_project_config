import os


class VariableNaming:
    """
    Class to standardize the naming convention of AWS resources like, username, groups and buckets and
    Herouku resources.
    """

    def __init__(self, project_slug, environment, *args, **kwargs):
        self.base_name = project_slug.replace('_', '-')
        self.environment = environment
        self.folder = kwargs.get('folder', None)

    def username(self):
        """AWS Username"""
        username = f'{self.base_name}-{self.environment}-user'
        return username

    def bucket_name(self):
        """AWS S3 bucket name"""
        bucket_name = f'{self.base_name}-{self.environment}-bucket'
        return bucket_name

    def group(self):
        """AWS Group name"""
        group = f'{self.base_name}-{self.environment}-group'
        return group

    def _build_filename(self, *args, folder=None):
        c_folder = self.folder
        if folder is not None:
            c_folder = folder
        base_name = '-'.join(args[0:-1])
        filename = f'{base_name}.{args[-1]}'
        if c_folder is not None:
            return os.path.join(c_folder, filename)
        return filename

    def policy_filename(self, folder=None):
        filename = self._build_filename(self.base_name, self.environment, 's3-policy', 'json', folder=folder)
        return filename

    def arn_script_filename(self, folder=None):
        filename = self._build_filename(self.base_name, self.environment, 'arn', 'sh', folder=folder)
        return filename

    def access_filename(self, folder=None):
        username = self.username()
        filename = self._build_filename(username, 'access', 'json', folder=folder)
        return filename

    def heroku_app_name(self):
        app_name = f'{self.base_name}-{self.environment}'
        return app_name

    def redis_name(self):
        redis = f'{self.base_name}-{self.environment}'
        return redis
