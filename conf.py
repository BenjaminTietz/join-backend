import os
import sys
import django

# Projektpfad hinzufügen
sys.path.insert(0, os.path.abspath('.'))  # adjust path  todo
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_join_backend_app.settings'  # adjust to project name  todo
django.setup()

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Join_Django_Rest_Framework_Backend'
copyright = '2024, Benjamin Tietz'
author = 'Benjamin Tietz'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

exclude_patterns = ['**/*.dist-info/LICENSE.rst']
