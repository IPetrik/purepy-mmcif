"""
Test cases for dictionary method management and invocation.

"""
from __future__ import absolute_import, print_function

import pytest
import sys

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path


from mmcif.api.MethodUtils import MethodUtils
from mmcif.io.IoAdapterPy import IoAdapterPy as IoAdapter

__docformat__ = "restructuredtext en"
__author__ = "Igor Petrik"
__email__ = "petrikigor@gmail.com"
__license__ = "Apache 2.0"

class TestMethodUtils():
    __slots__ = ()

    @pytest.fixture(scope = 'class')
    def test_paths(self, test_files, in_tmpdir):
        paths = dict(pathPdbxDataFile = test_files / "1kip.cif", 
                     pathPdbxDictFile = test_files / "mmcif_pdbx_v5_next_w_methods.dic", 
                     pathOutFile = Path("test-after-invoke-methods.cif"))
        return paths

    def test_get_dictionary_methods(self, test_paths):
        myIo = IoAdapter()
        dictContainerList = myIo.readFile(inputFilePath=test_paths['pathPdbxDictFile'])
        mU = MethodUtils(dictContainerList=dictContainerList)
        mU.dumpMethods(fh=sys.stdout)
        mD = mU.getMethods()
        assert len(mD) == 5

    def test_invoke_dictionary_methods(self, test_paths):
        myIo = IoAdapter()
        dictContainerList = myIo.readFile(inputFilePath=test_paths['pathPdbxDictFile'])
        mU = MethodUtils(dictContainerList=dictContainerList)

        dataContainerList = myIo.readFile(inputFilePath=test_paths['pathPdbxDataFile'])
        mU.setDataContainerList(dataContainerList=dataContainerList)

        mU.invokeMethods()
        print("Write data file after invoking methods")
        dataContainerList = mU.getDataContainerList()
        ok = myIo.writeFile(outputFilePath=test_paths['pathOutFile'], 
                            containerList=dataContainerList)
        assert ok

