import os
import sys


sys.path.insert(0, os.path.abspath('../')) 
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_join_backend_app.settings'


import django
django.setup()

project = 'Join Backend'
copyright = '2024, Benjamin Tietz'
author = 'Benjamin Tietz'
release = '2024'



extensions = [
    'sphinx.ext.autodoc',     
    'sphinx.ext.viewcode',    
    'sphinx.ext.napoleon',    
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


html_theme = 'alabaster'
html_static_path = ['_static']
