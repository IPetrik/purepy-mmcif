"""
Tests cases for Dictionary API.

"""
from __future__ import absolute_import, print_function

import pytest

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from mmcif.api.DictionaryApi import DictionaryApi
from mmcif.api.PdbxContainers import CifName
from mmcif.io.IoAdapterPy import IoAdapterPy as IoAdapter

__docformat__ = "restructuredtext en"
__author__ = "Igor Petrik"
__email__ = "petrikigor@gmail.com"
__license__ = "Apache 2.0"

class TestDictionaryApi():
    __slots__ = ()

    @pytest.fixture(scope = 'class')
    def api_paths(self, test_files):
        return dict(pathPdbxDictionary = test_files /  "mmcif_pdbx_v5_next.dic")

    def test_dump_enums(self, api_paths):
        myIo = IoAdapter(raiseExceptions=True)
        containerList = myIo.readFile(inputFilePath=api_paths['pathPdbxDictionary'])
        dApi = DictionaryApi(containerList=containerList, consolidate=True)
         
        eList = dApi.getEnumListAlt(category="pdbx_audit_support", attribute="country")
        print("Item %s Enum list sorted  %r\n" % ('country', eList))
        eList = dApi.getEnumListAlt(category="pdbx_audit_support", attribute="country", sortFlag=False)
        print("Item %s Enum list unsorted  %r\n" % ('country', eList))
        eList = dApi.getEnumListAltWithDetail(category="pdbx_audit_support", attribute="country")
        print("Item %s Enum with detail list  %r\n" % ('country', eList))
        assert len(eList) > 100

    def test_dump_index(self, api_paths):
        myIo = IoAdapter(raiseExceptions=True)
        containerList = myIo.readFile(inputFilePath=api_paths['pathPdbxDictionary'])
        dApi = DictionaryApi(containerList=containerList, consolidate=True)
        print("Index = %r\n" % dApi.getItemNameList('pdbx_nmr_spectral_dim'))
        print("Index = %r\n" % dApi.getAttributeNameList('pdbx_nmr_spectral_dim'))
        catIndex = dApi.getCategoryIndex()
        print("Index = %r\n" % catIndex['pdbx_nmr_spectral_dim'])
        assert catIndex['pdbx_nmr_spectral_dim'] is not None

    def test_dump_dictionary(self, api_paths):
        myIo = IoAdapter(raiseExceptions=True)
        containerList = myIo.readFile(inputFilePath=api_paths['pathPdbxDictionary'])
        dApi = DictionaryApi(containerList=containerList, consolidate=True)

        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
        groupList = dApi.getCategoryGroups()
        print('groupList %s\n' % groupList)
        for group in groupList:
            print('Group %s category list %s\n' % (group, dApi.getCategoryGroupCategories(groupName=group)))
        assert len(groupList) > 10

    def test_consolidate_dictionary(self, api_paths):
        myIo = IoAdapter(raiseExceptions=True)
        containerList = myIo.readFile(inputFilePath=api_paths['pathPdbxDictionary'])
        dApi = DictionaryApi(containerList=containerList, consolidate=True)

        for itemName in ['_entity.id', '_entity_poly_seq.num', '_atom_site.label_asym_id',
                         '_struct_asym.id', '_chem_comp.id', 'chem_comp_atom.comp_id', 'chem_comp_bond.comp_id']:
            categoryName = CifName.categoryPart(itemName)
            attributeName = CifName.attributePart(itemName)
            print("Full parent list for  %s : %s\n" % (itemName, dApi.getFullParentList(categoryName, attributeName)))
            print("Full child  list for  %s : %s\n" % (itemName, dApi.getFullChildList(categoryName, attributeName)))
            print("Ultimate parent for  %s : %s\n" % (itemName, dApi.getUltimateParent(categoryName, attributeName)))
            print("Type code for  %s : %s\n" % (itemName, dApi.getTypeCode(categoryName, attributeName)))
            self.assertIsNotNone(dApi.getTypeCode(categoryName, attributeName))

    def test_get_adjacent_categories(self, api_paths):
        """Test case -
        """
        myIo = IoAdapter(raiseExceptions=True)
        containerList = myIo.readFile(inputFilePath=api_paths['pathPdbxDictionary'])
        dApi = DictionaryApi(containerList=containerList, consolidate=True)

        cList = dApi.getCategoryList()
        cI = {}
        for c in cList:
            chL = dApi.getChildCategories(c)
            pL = dApi.getParentCategories(c)
            for ch in chL:
                if (ch, c) not in cI:
                    cI[(ch, c)] = 1
                else:
                    cI[(ch, c)] += 1
            for p in pL:
                if (c, p) not in cI:
                    cI[(c, p)] = 1
                else:
                    cI[(c, p)] += 1
        linkL = []
        for s, t in cI.keys():
            d = {'source': s, 'target': t, 'type': 'link'}
            linkL.append(d)

        assert len(linkL) == 50



