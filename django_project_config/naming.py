import os


class VariableNaming:

    def __init__(self, project_slug, environment, *args, **kwargs):
        self.base_name = project_slug.replace('_', '-')
        self.environment = environment
        self.folder = kwargs.get('folder', None)

    def username(self):
        username = f'{self.base_name}-{self.environment}-user'
        return username

    def bucket_name(self):
        bucket_name = f'{self.base_name}-{self.environment}-bucket'
        return bucket_name

    def group(self):
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
