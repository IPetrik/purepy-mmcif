# -*- coding: utf-8 -*-

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

import pytest

@pytest.fixture(scope = 'session')
def test_files():
    return Path(__file__).parent / 'data'

@pytest.fixture()
def in_tmpdir(monkeypatch, tmpdir):
    '''This fixture provides a temporary directory context in which
    the test will run. These temporary directories are typically in
    :file:`/tmp/pytest-of-<user>`, where this is one directory per 
    :program:`py.test` execution.'''
    monkeypatch.chdir(str(tmpdir))
    
    return tmpdir
