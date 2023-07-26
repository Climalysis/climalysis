# General information about the project.
project = u'Climalysis'
version = '0.0.1'

html_theme = 'alabaster'
html_theme_options = {
    'logo': '/images/climalysis_logo.png',
    'github_user': 'jake-casselman',
    'github_repo': 'Climalysis/climalysis',
    'github_button': True,
    'github_banner': True,
    'show_related': True,
    'note_bg': '#FFF59C'
}

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
]
