"""
Test implementing PDBx/mmCIF write and formatting operations.

"""
from __future__ import absolute_import, print_function

import pytest

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from mmcif.api.DataCategory import DataCategory
from mmcif.api.PdbxContainers import DataContainer
from mmcif.io.PdbxReader import PdbxReader
from mmcif.io.PdbxWriter import PdbxWriter

__docformat__ = "restructuredtext en"
__author__ = "Igor Petrik"
__email__ = "petrikigor@gmail.com"
__license__ = "Apache 2.0"

class TestPdbxWriter():
    __slots__ = ()

    @pytest.fixture(scope = 'class')
    def writer_paths(self, test_files, in_tmpdir):
        return dict(pathPdbxDataFile = test_files / "1kip.cif", 
                    pathBigPdbxDataFile = test_files / "1ffk.cif", 
                    pathOutputFile1 = Path("testOutputDataFile.cif"),
                    pathOutputFile2 = Path("testOutputDataFile.cif"))

    def test_write_data_file(self, writer_paths):
        myDataList = []

        curContainer = DataContainer("myblock")
        aCat = DataCategory("pdbx_seqtool_mapping_ref")
        aCat.appendAttribute("ordinal")
        aCat.appendAttribute("entity_id")
        aCat.appendAttribute("auth_mon_id")
        aCat.appendAttribute("auth_mon_num")
        aCat.appendAttribute("pdb_chain_id")
        aCat.appendAttribute("ref_mon_id")
        aCat.appendAttribute("ref_mon_num")
        aCat.append((1, 2, 3, 4, '55555555555555555555555555555555555555555555', 6, 7))
        aCat.append((1, 2, 3, 4, '5555', 6, 7))
        aCat.append((1, 2, 3, 4, '5555555555', 6, 7))
        aCat.append((1, 2, 3, 4, '5', 6, 7))
        curContainer.append(aCat)
        myDataList.append(curContainer)
        with open(writer_paths['pathOutputFile1'], "w") as ofh:
            pdbxW = PdbxWriter(ofh)
            pdbxW.setAlignmentFlag(flag=True)
            pdbxW.write(myDataList)
        assert len(myDataList) == 1

    def test_update_data_file(self, writer_paths):
        myDataList = []

        curContainer = DataContainer("myblock")
        aCat = DataCategory("pdbx_seqtool_mapping_ref")
        aCat.appendAttribute("ordinal")
        aCat.appendAttribute("entity_id")
        aCat.appendAttribute("auth_mon_id")
        aCat.appendAttribute("auth_mon_num")
        aCat.appendAttribute("pdb_chain_id")
        aCat.appendAttribute("ref_mon_id")
        aCat.appendAttribute("ref_mon_num")
        aCat.append((1, 2, 3, 4, 5, 6, 7))
        aCat.append((1, 2, 3, 4, 5, 6, 7))
        aCat.append((1, 2, 3, 4, 5, 6, 7))
        aCat.append((1, 2, 3, 4, 5, 6, 7))
        curContainer.append(aCat)
        myDataList.append(curContainer)
        with open(writer_paths['pathOutputFile1'], "w") as ofh:
            pdbxW = PdbxWriter(ofh)
            pdbxW.write(myDataList)
        #
        # Read and update the data -
        #
        myDataList = []
        with open(writer_paths['pathOutputFile1'], "r") as ifh:
            pRd = PdbxReader(ifh)
            pRd.read(myDataList)
        #
        myBlock = myDataList[0]
        # myBlock.printIt()
        myCat = myBlock.getObj('pdbx_seqtool_mapping_ref')
        # myCat.printIt()
        for iRow in range(0, myCat.getRowCount()):
            myCat.setValue('some value', 'ref_mon_id', iRow)
            myCat.setValue(100, 'ref_mon_num', iRow)
        with open(writer_paths['pathOutputFile2'], "w") as ofh:
            pdbxW = PdbxWriter(ofh)
            pdbxW.write(myDataList)
        assert len(myDataList) == 1

    def test_read_write_data_file(self, writer_paths):
        myDataList = []
        with open(writer_paths['pathPdbxDataFile'], "r") as ifh:
            pRd = PdbxReader(ifh)
            pRd.read(myDataList)

        with open(writer_paths['pathOutputFile1'], "w") as ofh:
            pWr = PdbxWriter(ofh)
            pWr.write(myDataList)

        assert len(myDataList) == 1
