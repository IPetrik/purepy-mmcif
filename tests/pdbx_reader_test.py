"""
Test cases for reading PDBx/mmCIF data files PdbxReader class -

"""
from __future__ import absolute_import, print_function



import pytest

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from mmcif.io.PdbxReader import PdbxReader

__docformat__ = "restructuredtext en"
__author__ = "Igor Petrik"
__email__ = "petrikigor@gmail.com"
__license__ = "Apache 2.0"

class TestPdbxReader():
    __slots__ = ()

    @pytest.fixture(scope = 'class')
    def reader_paths(self, test_files):
        return dict(pathPdbxDataFile = test_files / "1kip.cif", 
                    pathBigPdbxDataFile = test_files / "1ffk.cif",
                    pathSFDataFile = test_files / "example_sf.cif")

    def test_read_small_data_file(self, reader_paths):
        myDataList = []
        ifh = open(str(reader_paths['pathPdbxDataFile']), "r")
        pRd = PdbxReader(ifh)
        pRd.read(myDataList)
        ifh.close()
        #
        assert len(myDataList) == 1

    def test_read_big_data_file(self, reader_paths):
        myDataList = []
        ifh = open(str(reader_paths['pathBigPdbxDataFile']), "r")
        pRd = PdbxReader(ifh)
        pRd.read(myDataList)
        ifh.close()
        assert len(myDataList) == 1

    def testReadSFDataFile(self, reader_paths):
        myContainerList = []
        ifh = open(str(reader_paths['pathSFDataFile']), "r")
        pRd = PdbxReader(ifh)
        pRd.read(myContainerList)
        c0 = myContainerList[0]
        #
        catObj = c0.getObj("refln")
        if catObj is None:
            return False

        # nRows = catObj.getRowCount()
        #
        # Get column name index.
        #
        itDict = {}
        itNameList = catObj.getItemNameList()
        for idxIt, itName in enumerate(itNameList):
            itDict[str(itName).lower()] = idxIt
            #
        idf = itDict['_refln.f_meas_au']
        idsigf = itDict['_refln.f_meas_sigma_au']
        minR = 100
        maxR = -1
        sumR = 0
        icount = 0
        for row in catObj.getRowList():
            try:
                f = float(row[idf])
                sigf = float(row[idsigf])
                ratio = sigf / f
                # self.lfh.write(" %f %f %f\n" % (f,sigf,ratio))
                maxR = max(maxR, ratio)
                minR = min(minR, ratio)
                sumR += ratio
                icount += 1
            except Exception:
                continue

        ifh.close()
        print("f/sig(f) min %f max %f avg %f count %d\n" % (minR, maxR, sumR / icount, icount))
        assert icount == 99242


