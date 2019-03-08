"""
Test cases for simple star file reader/writer  --

"""
from __future__ import absolute_import, print_function

import pytest

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from mmcif.io.IoAdapterPy import IoAdapterPy as IoAdapter

__docformat__ = "restructuredtext en"
__author__ = "Igor Petrik"
__email__ = "petrikigor@gmail.com"
__license__ = "Apache 2.0"

class TestStarReader():
    __slots__ = ()
    
    @pytest.fixture(scope = 'class')
    def star_files_list(self, test_files):
        return (test_files / "chemical_shifts_example.str", test_files / "CCPN_H1GI.nef")

    def test_read_star_file(self, in_tmpdir, star_files_list):
        for fp in star_files_list:
            myIo = IoAdapter()
            containerList = myIo.readFile(inputFilePath=fp)
            print("container list is  %r\n" % ([(c.getName(), c.getType()) for c in containerList]))
            for c in containerList:
                c.setType('data')
            ofn = Path(fp.stem + '.cif')
            ok = myIo.writeFile(outputFilePath=ofn, containerList=containerList[1:])
            assert ok

    def test_read_write_star_file(self, in_tmpdir, star_files_list):
        for fp in star_files_list:
            myIo = IoAdapter()
            containerList = myIo.readFile(inputFilePath=fp)
            #
            # containerList is a flat list of containers in the order parsed.
            #
            # Create an index from the linear list data_ save_ sections and names --
            #
            # There can multiple data blocks where each data section is followed
            # by save frames --    Names can be repeated and the application must
            # create an appropriate index of the data and save sections according
            # it own requirements.
            #
            #
            iD = {}
            iDN = {}
            dL = []
            for container in containerList:
                if container.getType() == "data":
                    dL.append(container)
                    if container.getName() not in iD:
                        curContainerName = container.getName()
                        iD[curContainerName] = []
                        iDN[curContainerName] = []
                    else:
                        print("Duplicate data block %s\n" % container.getName())
                else:
                    iD[curContainerName].append(container)
                    iDN[curContainerName].append(container.getName())
            #
            # get the reference data out of the 2nd  data block --
            #
            if len(dL) > 1:
                c1 = dL[1]
                if 'chemical_shift_reference_1' in iDN[c1.getName()]:
                    idx = iDN[c1.getName()].index('chemical_shift_reference_1')
                    sf0 = iD[c1.getName()][idx]
                    catObj = sf0.getObj('Chem_shift_ref')
                    aL = catObj.getAttributeList()
                    rowL = catObj.getRowList()
                    print("Attribute list %s\n" % aL)
                    rowL = catObj.getRowList()
                    for ii, row in enumerate(rowL):
                        print("  %4d  %r\n" % (ii, row))
            ofn = Path(fp.stem + '.out')
            ok = myIo.writeFile(outputFilePath=ofn, containerList=containerList, useStopTokens=True)
            assert ok
