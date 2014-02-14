needs_sphinx = '1.1'

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.pngmath', 'numpydoc',
              'sphinx.ext.intersphinx', 'sphinx.ext.coverage',
              'sphinx.ext.autosummary', 'matplotlib.sphinxext.plot_directive']

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'Nansat'
copyright = u'2013, Nansen Center'
version = '0.1'
release = '0.1'
exclude_patterns = ['_build']
pygments_style = 'sphinx'

# 'class', 'init' or 'both'
autoclass_content = 'init'

# Whether to create a Sphinx table of contents for the lists of class methods and attributes.
# If a table of contents is made, Sphinx expects each entry to have a separate page.
#numpydoc_class_members_toctree = False

# Whether to show all members of a class
# in the Methods and Attributes sections automatically.
numpydoc_show_class_members = True

# -- Options for HTML output ---------------------------------------------------

html_theme = 'scipy'
html_theme_path = ['_theme']
#html_logo = '_static/scipyshiny_small.png'
html_static_path = ['../_static']
html_theme_options = {
    "edit_link": False,
    "sidebar": None,
    "scipy_org_logo": True,
    'navigation_links': True,
    "rootlinks": [],
}

pngmath_latex_preamble = r"""
\usepackage{color}
\definecolor{textgray}{RGB}{51,51,51}
\color{textgray}
"""
pngmath_use_preview = True
pngmath_dvipng_args = ['-gamma 1.5', '-D 96', '-bg Transparent']

html_use_modindex = True
html_use_index = True
html_show_sourcelink = True

'''
numpydoc_class_members_toctree = True
numpydoc_show_class_members = True
numpydoc_edit_link = True
numpydoc_use_plots = True
'''

#------------------------------------------------------------------------------
# Plot style
#------------------------------------------------------------------------------

plot_pre_code = """
import numpy as np
import scipy as sp
np.random.seed(123)
"""
plot_include_source = True
plot_formats = [('png', 96), 'pdf']
plot_html_show_formats = False

import math
phi = (math.sqrt(5) + 1)/2

font_size = 13*72/96.0  # 13 px

plot_rcparams = {
    'font.size': font_size,
    'axes.titlesize': font_size,
    'axes.labelsize': font_size,
    'xtick.labelsize': font_size,
    'ytick.labelsize': font_size,
    'legend.fontsize': font_size,
    'figure.figsize': (3*phi, 3),
    'figure.subplot.bottom': 0.2,
    'figure.subplot.left': 0.2,
    'figure.subplot.right': 0.9,
    'figure.subplot.top': 0.85,
    'figure.subplot.wspace': 0.4,
    'text.usetex': False,
}
