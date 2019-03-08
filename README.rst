.. image:: https://travis-ci.com/IPetrik/purepy-mmcif.svg?branch=master
    :target: https://travis-ci.com/IPetrik/purepy-mmcif

mmCIF Core Access Library
=========================

Introduction
------------

This module includes a native Python mmCIF API for data files.

Installation
------------

Download the library source software from the project repository:

.. code-block:: bash

   git clone https://github.com/ipetrik/purepy-mmcif.git

Optionally, run test suite using the Tox test runner. 

.. code-block:: bash

   tox

Installation is via the program [pip](https://pypi.python.org/pypi/pip).

.. code-block:: bash

   pip install .

To generate API documentation using [Sphinx](http://www.sphinx-doc.org/):

.. code-block:: bash

   cd scripts
   # Check Sphinx dependencies in the introductory comments to the following script.
   ./initdocs.sh
