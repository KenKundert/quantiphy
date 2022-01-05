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
    version = '2.17.0',
    description = 'physical quantities (numbers with units)',
    long_description = readme,
    long_description_content_type = 'text/x-rst',
    author = "Ken Kundert",
    author_email = 'quantiphy@nurdletech.com',
    url = 'https://quantiphy.readthedocs.io',
    download_url = 'https://github.com/kenkundert/quantiphy/tarball/master',
    license = 'MIT',
    py_modules = 'quantiphy'.split(),
    install_requires = [],
    python_requires = '>=3.5',
    zip_safe = True,
    keywords = keywords.split(),
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering',
    ],
)
