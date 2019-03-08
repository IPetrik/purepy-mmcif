"""  Various tests cases for PDBx/mmCIF data file and dictionary reader and writer.
"""

from __future__ import absolute_import

import pytest

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from mmcif.api.DataCategory import DataCategory
from mmcif.api.DataCategoryBase import DataCategoryBase
from mmcif.api.PdbxContainers import DataContainer
from mmcif.io.PdbxReader import PdbxReader
from mmcif.io.PdbxWriter import PdbxWriter

from six.moves import range

__docformat__ = "restructuredtext en"
__author__ = "Igor Petrik"
__email__ = "petrikigor@gmail.com"
__license__ = "Apache 2.0"

class TestPdbxReadWrite():
    __slots__ = ()

    @pytest.fixture(scope = 'class')
    def rw_data(self, test_files, in_tmpdir):
        data = dict(pathPdbxDataFile = test_files / "specialTestFile.cif", 
                    pathBigPdbxDataFile = test_files / "1ffk.cif",
                    pathOutputFile1 = Path("testOutputDataFile1.cif"),
                    pathOutputFile2 = Path("testOutputDataFile2.cif"),
                    pathOutputFile3 = Path("testOutputDataFileStopToken3.cif"),
                    pathOutputFile4 = Path("testOutputDataFile4.cif"),
                    pathOutputFile5 = Path("testOutputDataFile5.cif"),
                    pathTestFile = test_files / "test_single_row.cif",
                    pathTestFileStop = test_files / "testFileWithStopTokens.cif")
        return data

    def test_single_row(self, rw_data):
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
            aCat.appendAttribute("details")
            aCat.append([1, 2, 3, 4, 5, 6, 7, 'data_my_big_data_file'])
            aCat.append([1, 2, 3, 4, 5, 6, 7, 'loop_my_big_data_loop'])
            aCat.append([1, 2, 3, 4, 5, 6, 7, 'save_my_big_data_saveframe'])
            aCat.append([1, 2, 3, 4, 5, 6, 7, '_category.item'])

            curContainer.append(aCat)

            bCat = curContainer.getObj("pdbx_seqtool_mapping_ref")
            print("----attribute list %r\n" % bCat.getAttributeList())
            row = bCat.getRow(0)
            print("----ROW %r\n" % row)

            with open(rw_data['pathOutputFile2'], "w") as ofh:
                myDataList.append(curContainer)
                pdbxW = PdbxWriter(ofh)
                pdbxW.write(myDataList)

            assert len(myDataList) == 1

    def test_single_row_file(self, rw_data):
            myDataList = []
            ifh = open(rw_data['pathTestFile'], "r")
            pRd = PdbxReader(ifh)
            pRd.read(myDataList)
            ifh.close()

            myBlock = myDataList[0]
            myCat = myBlock.getObj('symmetry')
            print("----attribute list %r\n" % myCat.getAttributeList())
            row = myCat.getRow(0)
            print("----ROW %r\n" % row)
            #
            # myCat.dumpIt()

            with open(rw_data['pathOutputFile2'], "w") as ofh:
                pdbxW = PdbxWriter(ofh)
                pdbxW.write(myDataList)

            assert len(myDataList) == 1

    def test_row_list_initialization(self, rw_data):
            fn = rw_data['pathOutputFile4']
            attributeNameList = ['aOne', 'aTwo', 'aThree', 'aFour', 'aFive', 'aSix', 'aSeven', 'aEight', 'aNine', 'aTen']
            rowList = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                       ]
            nameCat = 'myCategory'

            curContainer = DataContainer("myblock")
            aCat = DataCategory(nameCat, attributeNameList, rowList)
            curContainer.append(aCat)

            myContainerList = []
            myContainerList.append(curContainer)
            ofh = open(fn, "w")
            pdbxW = PdbxWriter(ofh)
            pdbxW.write(myContainerList)
            ofh.close()

            myContainerList = []
            ifh = open(fn, "r")
            pRd = PdbxReader(ifh)
            pRd.read(myContainerList)
            ifh.close()
            for container in myContainerList:
                for objName in container.getObjNameList():
                    name, aList, rList = container.getObj(objName).get()
                    print("Recovered data category  %s\n" % name)
                    print("Attribute list           %r\n" % repr(aList))
                    print("Row list                 %r\n" % repr(rList))
            assert len(myContainerList) == 1

    def test_write_data_file(self, rw_data):
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
            aCat.append([1, 2, 3, 4, 5, 6, 7])
            aCat.append([1, 2, 3, 4, 5, 6, 7])
            aCat.append([1, 2, 3, 4, 5, 6, 7])
            aCat.append([1, 2, 3, 4, 5, 6, 7])
            aCat.append([7, 6, 5, 4, 3, 2, 1])
            curContainer.append(aCat)

            myDataList.append(curContainer)
            with open(rw_data['pathOutputFile1'], "w") as ofh:
                pdbxW = PdbxWriter(ofh)
                pdbxW.write(myDataList)
            assert len(myDataList) == 1

    def test_update_data_file(self, rw_data):
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
            aCat.append([9, 2, 3, 4, 5, 6, 7])
            aCat.append([10, 2, 3, 4, 5, 6, 7])
            aCat.append([11, 2, 3, 4, 5, 6, 7])
            aCat.append([12, 2, 3, 4, 5, 6, 7])

            curContainer.append(aCat)
            myDataList.append(curContainer)
            ofh = open(rw_data['pathOutputFile1'], "w")
            pdbxW = PdbxWriter(ofh)
            pdbxW.write(myDataList)
            ofh.close()

            myDataList = []
            ifh = open(rw_data['pathOutputFile1'], "r")
            pRd = PdbxReader(ifh)
            pRd.read(myDataList)
            ifh.close()
            myBlock = myDataList[0]
            myCat = myBlock.getObj('pdbx_seqtool_mapping_ref')
            for iRow in range(0, myCat.getRowCount()):
                myCat.setValue('some value', 'ref_mon_id', iRow)
                myCat.setValue(100, 'ref_mon_num', iRow)

            with open(rw_data['pathOutputFile2'], "w") as ofh:
                pdbxW = PdbxWriter(ofh)
                pdbxW.write(myDataList)

            assert len(myDataList) == 1

    def test_read_data_file(self, rw_data):
            myDataList = []
            ifh = open(rw_data['pathPdbxDataFile'], "r")
            pRd = PdbxReader(ifh)
            pRd.read(myDataList)
            ifh.close()
            assert len(myDataList) == 1

    def test_read_write_data_file(self, rw_data):
            myDataList = []
            with open(rw_data['pathPdbxDataFile'], "r") as ifh:
                pRd = PdbxReader(ifh)
                pRd.read(myDataList)

            with open(rw_data['pathOutputFile1'], "w") as ofh:
                pWr = PdbxWriter(ofh)
                pWr.write(myDataList)
            assert len(myDataList) == 1

    def test_read_write_list_accessors(self, rw_data):
            dc = DataCategoryBase('test', attributeNameList=['a', 'b', 'c', 'd'])

            dc.append([1, 2, 3, 4])
            dc.append([1, 2, 3, 4])
            dc.append([1, 2, 3, 4])
            dc.append([1, 2, 3, 4, 5, 6, 7])
            dc.append([1, 2, 3, 4])

            dc.insert(0, [4, 3, 2, 1])

            print("Full  %r\n" % dc)
            print("slice %r\n" % dc[2:4])
            print("last  %r\n" % dc[-1])

            for r in dc:
                print("row data %r\n" % r)

            dc.setMapping('ATTRIBUTE')
            for r in dc:
                print("row attrib dict %r\n" % r)

            dc.setMapping('ITEM')
            for r in dc:
                print("row item dict %r\n" % r)

            dc.setMapping('DATA')

            print("row 3 %r\n" % dc[3])
            tmp = dc[3]
            dc[3] = []
            print("row 3 %r\n" % dc[3])
            dc[3] = tmp
            print("row 3 %r\n" % dc[3])

            dc.setMapping('ATTRIBUTE')
            tmp = dc[3]

            dt = {}
            for k, v in tmp.items():
                dt[k] = 10000
            print("row dict %r\n" % dt)

            dc[3] = dt
            print("row 3%r\n" % dc[3])
            dc[3] = tmp

            dc.setMapping('ITEM')
            tmp = dc[3]

            dt = {}
            for k, v in tmp.items():
                dt[k] = 10001
            print("row dict %r\n" % dt)

            dc[3] = dt
            print("row 3 %r\n" % dc[3])

            print("print raw     %r\n" % dc)
            print("print string  %s\n" % dc)

    def test_update_attribute(self, rw_data):
        ifn = rw_data['pathBigPdbxDataFile']
        ofn = rw_data['pathOutputFile2']
        myContainerList = []
        with open(ifn, "r") as ifh:
            pRd = PdbxReader(ifh)
            pRd.read(myContainerList)
        #
        dsId = "D_000000"
        atName = 'entry_id'
        for container in myContainerList:
            container.setName(dsId)
            # remove category citation
            container.remove('citation')
            for objName in container.getObjNameList():
                dcObj = container.getObj(objName)
                if dcObj.hasAttribute(atName):
                    for iRow in range(0, dcObj.getRowCount()):
                        dcObj.setValue(dsId, attributeName=atName, rowIndex=iRow)
                elif objName.lower() == 'entry':
                    dcObj.setValue(dsId, attributeName='id', rowIndex=0)

        #
        with open(ofn, "w") as ofh:
            pWr = PdbxWriter(ofh)
            pWr.write(myContainerList)
        assert len(myContainerList) == 1

    def test_read_write_data_file_stop(self, rw_data):
        myDataList = []
        with open(rw_data['pathTestFileStop'], "r") as ifh:
            pRd = PdbxReader(ifh)
            pRd.read(myDataList)

        with open(rw_data['pathOutputFile3'], "w") as ofh:
            pWr = PdbxWriter(ofh)
            pWr.write(myDataList)
        assert len(myDataList) == 1

    def test_row_dict_initialization(self, rw_data):
        rLen = 10
        fn = rw_data['pathOutputFile5']
        attributeNameList = ['a', 'b', 'c', 'd']
        rowList = [{'a': 1, 'b': 2, 'c': 3, 'd': 4} for i in range(rLen)]
        nameCat = 'myCategory'
        #
        #
        curContainer = DataContainer("myblock")
        aCat = DataCategory(nameCat, attributeNameList, rowList)
        aCat.append({'a': 1, 'b': 2, 'c': 3, 'd': 4})
        aCat.append({'a': 1, 'b': 2, 'c': 3, 'd': 4})
        aCat.extend(rowList)
        curContainer.append(aCat)
        aCat.renameAttributes({'a': 'aa', 'b': 'bb', 'c': 'cc', 'd': 'dd'})
        aCat.setName('renamedCategory')
        #
        #
        myContainerList = []
        myContainerList.append(curContainer)
        ofh = open(fn, "w")
        pdbxW = PdbxWriter(ofh)
        pdbxW.write(myContainerList)
        ofh.close()

        myContainerList = []
        ifh = open(fn, "r")
        pRd = PdbxReader(ifh)
        pRd.read(myContainerList)
        ifh.close()
        for container in myContainerList:
            for objName in container.getObjNameList():
                name, aList, rList = container.getObj(objName).get()
                print("Recovered data category  %s\n" % name)
                print("Attribute list           %r\n" % repr(aList))
                print("Row list                 %r\n" % repr(rList))
        assert len(myContainerList) == 1
        assert len(rList) == 2 * rLen + 2

