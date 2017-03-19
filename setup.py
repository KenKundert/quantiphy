try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

with open('README.rst') as f:
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
    version='1.3.0',
    description='physical quantities (numbers with units)',
    long_description=readme,
    author="Ken Kundert",
    author_email='quantiphy@nurdletech.com',
    url='http://nurdletech.com/linux-utilities/quantiphy',
    download_url='https://github.com/kenkundert/quantiphy/tarball/master',
    license='GPLv3+',
    zip_safe=True,
    py_modules='quantiphy'.split(),
    install_requires=dependencies.split(),
    setup_requires='pytest-runner>=2.0'.split(),
    tests_require='pytest'.split(),
    keywords=keywords.split(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering',
    ],
)
