import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

project = 'Optical Properties Scrapping'
copyright = '2024, Anibal T Bezerra'
author = 'Anibal T Bezerra'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
]

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

html_theme = 'sphinx_pdj_theme'

html_static_path = ['_static']
