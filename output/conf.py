extensions = [
    'sphinx_toolbox.confval'
]
source_suffix = '.rst'
master_doc = 'index'
project = u'Reference'
copyright = u'2021-2022, OSISM GmbH'
author = u'OSISM GmbH'
version = u''
release = u''
language = 'en'
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = True
html_theme = 'sphinx_rtd_theme'
html_show_sphinx = False
html_show_sourcelink = False
html_show_copyright = True
htmlhelp_basename = 'documentation'
html_theme_options = {
    'display_version': False,
    'canonical_url': 'https://docs.osism.tech/reference/',
    'style_external_links': True,
    'logo_only': True,
    'prev_next_buttons_location': None
}
html_context = {
    'display_github': True,
    'github_user': 'osism',
    'github_repo': 'openstack-configuration-reference',
    'github_version': 'main',
    'conf_py_path': '/output/'
}
html_logo = 'images/logo.png'
html_static_path = [
    '_static'
]
latex_elements = {}
