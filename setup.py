from setuptools import setup
import sys

with open('README.rst', encoding="UTF-8") as f:
    readme = f.read()

keywords='''
    quantities physical quantity units SI scale factors engineering notation
    mks cgs
'''

setup(
    name = 'quantiphy',
    version = '2.13.0',
    description = 'physical quantities (numbers with units)',
    long_description = readme,
    long_description_content_type = 'text/x-rst',
    author = "Ken Kundert",
    author_email = 'quantiphy@nurdletech.com',
    url = 'https://quantiphy.readthedocs.io',
    download_url = 'https://github.com/kenkundert/quantiphy/tarball/master',
    license = 'GPLv3+',
    zip_safe = False,
    py_modules = 'quantiphy'.split(),
    install_requires = [],
    tests_require = 'pytest inform rkm_codes'.split(),
    python_requires = '>=3.5',
    keywords = keywords.split(),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering',
    ],
)
