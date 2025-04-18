import os
import sys
sys.path.insert(0, os.path.abspath('../climalysis'))

project = 'Climalysis'
author = 'Jake Casselman'
release = '0.1.3'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'furo'
html_static_path = ['_static']
html_css_files = ['custom.css']
html_title = "Climalysis Docs"
html_logo = "_static/climalysis_logo.png"
html_theme_options = {
    "source_repository": "https://github.com/Climalysis/climalysis/",
    "source_branch": "main",
    "navigation_with_keys": True,
}
