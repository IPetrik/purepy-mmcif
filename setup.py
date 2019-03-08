# Copyright 2009-2019 John Westbrook (RCSB)
# Copyright 2019 Igor Petrik

from setuptools import find_packages, setup

thisPackage = 'purepy-mmcif'

setup(
    name=thisPackage,
    #version=version,

    use_scm_version=True,
    setup_requires=['setuptools_scm'],

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

    zip_safe=False,
)
