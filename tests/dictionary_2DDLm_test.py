"""
Tests cases for Dictionary API generating alternative DDLm metadata format.

"""
from __future__ import absolute_import, print_function

import pytest

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

from mmcif.api.DataCategory import DataCategory
from mmcif.api.DictionaryApi import DictionaryApi
from mmcif.api.PdbxContainers import (CifName, DataContainer,
                                      DefinitionContainer)
from mmcif.io.IoAdapterPy import IoAdapterPy

__docformat__ = "restructuredtext en"
__author__ = "Igor Petrik"
__email__ = "petrikigor@gmail.com"
__license__ = "Apache 2.0"

class TestDictionary2DDLm():
    __slots__ = ()

    def test_gen_ddlm(self, in_tmpdir, test_files):
        myIo = IoAdapterPy()
        containerList = myIo.readFile(inputFilePath=str(test_files / 'mmcif_pdbx_v5_next.dic'))
        dApi = DictionaryApi(containerList=containerList, consolidate=True)
        parentD = dApi.getParentDictionary()
        #
        oCList = []
        dDef = DataContainer('mmcif_pdbx_ddlm_auto')
        dc = DataCategory("dictionary")
        dc.appendAttribute("title")
        dc.appendAttribute("class")
        dc.appendAttribute("version")
        dc.appendAttribute("date")
        dc.appendAttribute("ddl_conformance")
        dc.appendAttribute("text")
        dc.append(['mmcif_pdbx_ddlm_auto', 'Instance', 'latest', '2018-03-09', 'ddlm best effort', 'Software converted PDBx dictionary using DDLm semantics'])
        dDef.append(dc)
        oCList.append(dDef)

        catIdx = dApi.getCategoryIndex()
        for catName in sorted(catIdx.keys()):
            attNameList = catIdx[catName]
            # created definition container -
            cDef = DefinitionContainer(catName)
            oCList.append(cDef)
            #
            dc = DataCategory("definition")
            dc.appendAttribute("id")
            dc.appendAttribute("scope")
            dc.appendAttribute("class")
            dc.appendAttribute("update")
            dc.append([catName, "Category", "Loop", "2018-03-09"])
            cDef.append(dc)
            val = dApi.getCategoryDescription(category=catName)
            dc = DataCategory("description")
            dc.appendAttribute("text")
            dc.append([val])
            cDef.append(dc)
            #
            dc = DataCategory("name")
            dc.appendAttribute("category_id")
            dc.appendAttribute("object_id")

            valList = dApi.getCategoryGroupList(category=catName)
            pcg = catName
            for val in valList:
                if val != 'inclusive_group':
                    pcg = val
                    break
            dc.append([catName, pcg])
            cDef.append(dc)

            valList = dApi.getCategoryKeyList(category=catName)
            if len(valList) < 1:
                print("Missing caegory key for category %s\n" % catName)
            else:
                dc = DataCategory("category")
                dc.appendAttribute("key_id")
                kItemName = CifName.itemName(catName, "synthetic_key")
                dc.append([kItemName])
                cDef.append(dc)

                iDef = DefinitionContainer(kItemName)
                self._makeKeyItem(catName, "synthetic_key", valList, iDef)
                oCList.append(iDef)

            for attName in attNameList:
                itemName = CifName.itemName(catName, attName)
                iDef = DefinitionContainer(itemName)

                oCList.append(iDef)

                #
                dc = DataCategory("definition")
                dc.appendAttribute("id")
                dc.appendAttribute("scope")
                dc.appendAttribute("class")
                dc.appendAttribute("update")
                dc.append([itemName, "Item", "Single", "2013-08-22"])
                iDef.append(dc)
                #
                val = dApi.getDescription(category=catName, attribute=attName)
                dc = DataCategory("description")
                dc.appendAttribute("text")
                dc.append([val])
                iDef.append(dc)
                #
                dc = DataCategory("name")
                dc.appendAttribute("category_id")
                dc.appendAttribute("object_id")
                #
                if itemName in parentD:
                    dc.appendAttribute("linked_item_id")
                    dc.append([catName, attName, parentD[itemName][0]])
                else:
                    dc.append([catName, attName])
                iDef.append(dc)
                #
                #
                aliasList = dApi.getItemAliasList(category=catName, attribute=attName)
                if len(aliasList) > 0:
                    dc = DataCategory("alias")
                    dc.appendAttribute("definition_id")
                    for alias in aliasList:
                        dc.append([alias[0]])
                    iDef.append(dc)

                enList = dApi.getEnumListAltWithDetail(category=catName, attribute=attName)

                tC = dApi.getTypeCode(category=catName, attribute=attName)
                tcontainer = 'Single'
                purpose = 'Describe'
                source = 'Recorded'
                contents = 'Text'
                #
                if tC is None:
                    self.__lfh.write("Missing data type attribute %s\n" % attName)
                elif tC in ['code', 'atcode', 'name', 'idname', 'symop', 'fax', 'phone', 'email', 'code30', 'ec-type']:
                    purpose = 'Encode'
                    contents = 'Text'
                    source = 'Assigned'
                elif tC in ['ucode']:
                    purpose = 'Encode'
                    contents = 'Code'
                    source = 'Assigned'
                elif tC in ['line', 'uline', 'text']:
                    purpose = 'Describe'
                    source = 'Recorded'
                    contents = 'Text'
                elif tC in ['int']:
                    purpose = 'Number'
                    source = 'Recorded'
                    contents = 'Integer'
                elif tC in ['int-range']:
                    purpose = 'Number'
                    source = 'Recorded'
                    contents = 'Range'
                elif tC in ['float']:
                    purpose = 'Measurand'
                    source = 'Recorded'
                    contents = 'Real'
                elif tC in ['float-range']:
                    purpose = 'Measurand'
                    source = 'Recorded'
                    contents = 'Range'
                elif tC.startswith('yyyy'):
                    source = 'Assigned'
                    contents = 'Date'
                    purpose = 'Describe'

                if len(enList) > 0:
                    purpose = 'State'

                dc = DataCategory("type")
                dc.appendAttribute("purpose")
                dc.appendAttribute("source")
                dc.appendAttribute("contents")
                dc.appendAttribute("container")
                dc.append([purpose, source, contents, tcontainer])
                iDef.append(dc)
                #
                if (len(enList) > 0):
                    dc = DataCategory("enumeration_set")
                    dc.appendAttribute("state")
                    dc.appendAttribute("detail")
                    for en in enList:
                        dc.append([en[0], en[1]])
                    iDef.append(dc)

                dfv = dApi.getDefaultValue(category=catName, attribute=attName)
                bvList = dApi.getBoundaryList(category=catName, attribute=attName)
                if (((dfv is not None) and (dfv not in ['?', '.'])) or len(bvList) > 0):
                    row = []
                    dc = DataCategory("enumeration")
                    if dfv is not None:
                        dc.appendAttribute("default")
                        row.append(dfv)
                    if len(bvList) > 0:
                        dc.appendAttribute("range")
                        mminVp = -1000000
                        mmaxVp = 10000000
                        mminV = mmaxVp
                        mmaxV = mminVp
                        for bv in bvList:
                            minV = float(bv[0]) if bv[0] != '.' else mminVp
                            maxV = float(bv[1]) if bv[1] != '.' else mmaxVp
                            mminV = min(mminV, minV)
                            mmaxV = max(mmaxV, maxV)
                        if mminV == mminVp:
                            mminV = ''
                        if mmaxV == mmaxVp:
                            mmaxV = ''
                        row.append(str(mminV) + ":" + str(mmaxV))

                    dc.append(row)
                    iDef.append(dc)

        myIo.writeFile(outputFilePath="mmcif_pdbx_ddlm_auto.dic", containerList=oCList)

    def _makeKeyItem(self, catName, attName, keyItemList, iDef):
        itemName = CifName.itemName(catName, attName)

        #
        dc = DataCategory("definition")
        dc.appendAttribute("id")
        dc.appendAttribute("scope")
        dc.appendAttribute("class")
        dc.appendAttribute("update")
        dc.append([itemName, "Item", "Single", "2013-08-22"])
        iDef.append(dc)
        #
        dc = DataCategory("description")
        dc.appendAttribute("text")
        dc.append(['synthentic componsite key'])
        iDef.append(dc)
        #
        dc = DataCategory("name")
        dc.appendAttribute("category_id")
        dc.appendAttribute("object_id")
        dc.append([catName, attName])
        iDef.append(dc)
        tcontainer = 'Set'
        purpose = 'Composite'
        source = 'Derived'
        contents = 'Name'
        dimension = '[%d]' % len(keyItemList)
        #

        dc = DataCategory("type")
        dc.appendAttribute("purpose")
        dc.appendAttribute("source")
        dc.appendAttribute("contents")
        dc.appendAttribute("container")
        dc.appendAttribute("dimension")
        dc.append([purpose, source, contents, tcontainer, dimension])
        iDef.append(dc)

        dc = DataCategory("method")
        dc.appendAttribute("purpose")
        dc.appendAttribute("expression")

        tmpl = '''

                      With row as %s

                           %s = [%s]

        '''
        mText = tmpl % (catName, itemName, ','.join(keyItemList))
        dc.append(['Evaluation', mText])
        iDef.append(dc)
