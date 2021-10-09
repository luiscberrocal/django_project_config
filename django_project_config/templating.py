from jinja2 import Environment, PackageLoader, select_autoescape


class TemplateHelper:

    def __init__(self):
        self.env = Environment(
            loader=PackageLoader("django_project_config"),
            autoescape=select_autoescape()
        )

    def render(self, template_name, **kwargs):
        template = self.env.get_template(template_name)
        content = template.render(**kwargs)
        return content

    def write(self, filename, template_name, **kwargs):
        content = self.render(template_name, **kwargs)
        with open(filename, 'w') as file:
            file.write(content)

template_helper = TemplateHelper()