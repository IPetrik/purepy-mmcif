## mmCIF Core Access Library

### Introduction

This module includes a native Python mmCIF API for data files.

### Installation

Download the library source software from the project repository:

```bash

git clone  --recurse-submodules  https://github.com/ipetrik/purepy-mmcif.git

```

Optionally, run test suite using the Tox test runner. 

```bash
tox
```

Installation is via the program [pip](https://pypi.python.org/pypi/pip).

```bash
pip install .
```

To generate API documentation using [Sphinx](http://www.sphinx-doc.org/):

```bash
cd scripts
# Check Sphinx dependencies in the introductory comments to the following script.
./initdocs.sh

```
