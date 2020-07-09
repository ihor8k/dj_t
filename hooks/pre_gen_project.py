TERMINATOR = '\x1b[0m'
WARNING = '\x1b[1;33m [WARNING]: '
INFO = '\x1b[1;33m [INFO]: '
HINT = '\x1b[3;33m'
SUCCESS = '\x1b[1;32m [SUCCESS]: '

project_slug = '{{ cookiecutter.project_slug }}'
if hasattr(project_slug, 'isidentifier'):
    assert project_slug.isidentifier(), f'{project_slug} project slug is not a valid Python identifier.'

assert project_slug == project_slug.lower(), f'{project_slug} project slug should be all lowercase'
