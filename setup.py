try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from codecs import open
import sys

with open('README.rst', encoding="UTF-8") as f:
    readme = f.read()

if sys.version_info < (3,3):
    dependencies='six chainmap'
else:
    dependencies='six'
keywords='''
    quantities physical quantity units SI scale factors engineering notation
    mks cgs
'''

setup(
    name='quantiphy',
    version='2.10.0',
    description='physical quantities (numbers with units)',
    long_description=readme,
    long_description_content_type='text/x-rst',
    author="Ken Kundert",
    author_email='quantiphy@nurdletech.com',
    url='https://quantiphy.readthedocs.io',
    download_url='https://github.com/kenkundert/quantiphy/tarball/master',
    license='GPLv3+',
    zip_safe=True,
    py_modules='quantiphy'.split(),
    install_requires=dependencies.split(),
    setup_requires='pytest-runner>=2.0'.split(),
    tests_require='pytest'.split(),
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*',
    keywords=keywords.split(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3.3',
        #    should work, but no longer tested
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering',
    ],
)
