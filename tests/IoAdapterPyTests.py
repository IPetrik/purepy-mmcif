"""
Test cases for reading and updating PDBx data files using Python Wrapper
IoAdapterCore wrapper which provides an API to the C++ CifFile class
library of file and dictionary tools that is conforms to our Native
Python library.
"""
from __future__ import absolute_import, print_function

import pytest

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from mmcif.io.IoAdapterPy import IoAdapterPy as IoAdapter
from mmcif.io.PdbxReader import PdbxError, SyntaxError

__docformat__ = "restructuredtext en"
__author__ = "Igor Petrik"
__email__ = "petrikigor@gmail.com"
__license__ = "Apache 2.0"

class TestIoAdapter():
    __slots__ = ()
    
    @pytest.fixture(scope = 'class')
    def io_data(self, test_files, in_tmpdir):
        inputs = {}

        inputs['pathPdbxDataFile'] = test_files / "1kip.cif"
        inputs['pathBigPdbxDataFile'] = test_files / "1ffk.cif.gz"
        inputs['pathPdbxDictFile'] = test_files / "mmcif_pdbx_v5_next.dic"
        inputs['testBlockCount'] = 7350
        inputs['pathErrPdbxDataFile'] = test_files / "1bna-errors.cif"
        inputs['pathQuotesPdbxDataFile'] = test_files / "specialTestFile.cif"
        #
        inputs['pathOutputPdbxFile'] = Path("myPdbxOutputFile.cif")
        inputs['pathOutputPdbxFileSelect'] = Path("myPdbxOutputFileSelect.cif")
        inputs['pathOutputPdbxFileExclude'] = Path("myPdbxOutputFileExclude.cif")
        #
        inputs['pathQuotesOutputPdbxFile'] = Path("myPdbxQuotesOutputFile.cif")
        inputs['pathBigOutputDictFile'] = Path("myDictOutputFile.cif")

        inputs['pathMissingFile'] = test_files / "unicode-test-missing.cif"
        #
        inputs['pathUnicodePdbxFile'] = test_files / "unicode-test.cif"
        inputs['pathCharRefPdbxFile'] = test_files / "unicode-char-ref-test.cif"
        #
        inputs['pathOutputUnicodePdbxFile'] = Path("out-unicode-test.cif")
        inputs['pathOutputCharRefPdbxFile'] = Path("out-unicode-char-ref-test.cif")

        inputs['pathOutputDir'] = Path()
        
        return inputs

    @pytest.mark.parametrize('fp_key, enforceAscii',
                             [('pathPdbxDataFile', False), 
                              ('pathBigPdbxDataFile', False), 
                              ('pathQuotesPdbxDataFile', False), 
                              ('pathUnicodePdbxFile', False), 
                              ('pathPdbxDataFile', True), 
                              ('pathBigPdbxDataFile', True), 
                              ('pathQuotesPdbxDataFile', True)])
    def testFileReader(self, io_data, fp_key, enforceAscii):
        io = IoAdapter(raiseExceptions=True)
        containerList = io.readFile(io_data[fp_key], 
                                    enforceAscii=enforceAscii, 
                                    outDirPath=io_data['pathOutputDir'])
        print ("Read %d data blocks" % len(containerList))
        assert len(containerList) == 1

    @pytest.mark.parametrize('fp_key', 
                             ['pathPdbxDictFile', 'pathPdbxDictFile'])
    def test_dict_reader(self, io_data, fp_key):
        io = IoAdapter(raiseExceptions=True)
        containerList = io.readFile(io_data[fp_key], enforceAscii=False, 
                                    outDirPath=io_data['pathOutputDir'])
        print("Read %d data blocks" % len(containerList))
        assert len(containerList) > io_data['testBlockCount']

    @pytest.mark.parametrize('fp_key', 
                             ['pathErrPdbxDataFile', 'pathErrPdbxDataFile'])
    def test_file_reader_exception_handler_1(self, io_data, fp_key):
        io = IoAdapter(raiseExceptions=True)
        print (io_data)
        with pytest.raises(SyntaxError):
            io.readFile(io_data[fp_key], enforceAscii=False, 
                        outDirPath=io_data['pathOutputDir'])

    @pytest.mark.parametrize('fp_key, expected_exc, enforceAscii', 
                             [('pathMissingFile', PdbxError, True),])
    def test_file_reader_exception_handler_2(self, io_data, fp_key, expected_exc, 
                                        enforceAscii):
        with pytest.raises(expected_exc):
            io = IoAdapter(raiseExceptions=True, readEncodingErrors='ignore')
            containerList = io.readFile(io_data[fp_key], 
                                        enforceAscii=enforceAscii, 
                                        outDirPath=io_data['pathOutputDir'])
            print ("Containerlist length %d " % len(containerList))

    @pytest.mark.parametrize('ifp_key, ofp_key, enforceAscii', 
                             [('pathBigPdbxDataFile', 'pathOutputPdbxFile', True),
                              ('pathPdbxDictFile', 'pathBigOutputDictFile', True), 
                              ('pathQuotesPdbxDataFile', 'pathQuotesOutputPdbxFile', True), 
                              ('pathUnicodePdbxFile', 'pathOutputUnicodePdbxFile', False), 
                              ('pathCharRefPdbxFile', 'pathOutputCharRefPdbxFile', False)])
    def test_file_reader_writer(self, io_data, ifp_key, ofp_key, enforceAscii):
        io = IoAdapter(raiseExceptions=True, useCharRefs=enforceAscii)
        containerList = io.readFile(io_data[ifp_key])
        print ("Read %d data blocks" % len(containerList))
        ok = io.writeFile(io_data[ofp_key], containerList=containerList, 
                          enforceAscii=enforceAscii)
        assert ok

    @pytest.mark.parametrize('ifp_key, ofp_key, selectList, excludeFlag',
                              [('pathBigPdbxDataFile', 'pathOutputPdbxFileSelect', ['atom_site'], False), 
                                ('pathBigPdbxDataFile', 'pathOutputPdbxFileExclude', ['atom_site'], True)])
    def test_file_reader_writer_select(self, io_data, ifp_key, ofp_key, selectList, excludeFlag):
        io = IoAdapter(raiseExceptions=False, useCharRefs=True)
        containerList = io.readFile(io_data[ifp_key], enforceAscii=True, 
                                    selectList=selectList, 
                                    excludeFlag=excludeFlag, 
                                    outDirPath=io_data['pathOutputDir'])
        print ("Read %d data blocks" % len(containerList))
        ok = io.writeFile(io_data[ofp_key], containerList=containerList, 
                          enforceAscii=True)
        assert ok

