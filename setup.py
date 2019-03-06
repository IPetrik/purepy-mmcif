# File: setup.py
# Date: 17-Dec-2017
#
# Update:  17-Jan-2018 jdw - resolve python virtual env issues with Tox.
#           8-Aug-2018 jdw - add py3.7
#
import re

from setuptools import find_packages, setup

thisPackage = 'purepy-mmcif'

with open('mmcif/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name=thisPackage,
    version=version,
    description='A python-only fork of the RCSB mmCIF Core Access Library',
    long_description="See:  README.md",
    author='Igor Petrik',
    author_email='petrikigor@gmail.com',
    url='https://github.com/ipetrik/purepy-mmcif',

    license='Apache 2.0',
    classifiers=(
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ),

    install_requires=['future', 'six'],
    packages=find_packages(exclude=['mmcif.tests', 'tests.*']),
    package_data={
        # If any package contains *.md or *.rst ...  files, include them:
        '': ['*.md', '*.rst', "*.txt"],
    },

    test_suite="mmcif.tests",
    tests_require=['tox'],

    # Not configured ...
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    # Added for
    command_options={
        'build_sphinx': {
            'project': ('setup.py', thisPackage),
            'version': ('setup.py', version),
            'release': ('setup.py', version)
        }
    },
    zip_safe=False,
)
