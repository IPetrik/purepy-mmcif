# -*- coding: utf-8 -*-

"""
Test cases for data category container classes.

"""
from __future__ import absolute_import, print_function

import pytest

from itertools import chain, islice, repeat

from mmcif.api.DataCategory import DataCategory
from mmcif.api.DataCategoryBase import DataCategoryBase

__docformat__ = "restructuredtext en"
__author__ = "Igor Petrik"
__email__ = "petrikigor@gmail.com"
__license__ = "Apache 2.0"

def window(seq, size=2, fill=0, fill_left=False, fill_right=False):
    """ Returns a sliding window (of width n) over data from the iterable:
      s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
    """
    ssize = size - 1
    it = chain(
        repeat(fill, ssize * fill_left),
        iter(seq),
        repeat(fill, ssize * fill_right))
    result = tuple(islice(it, size))
    if len(result) == size:  # `<=` if okay to return seq if len(seq) < size
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


class TestDataCategory():
    __slots__ = ()
    
    @pytest.fixture(scope = 'class')
    def category_data(self):
        inputs = {}
        inputs ['attributeList'] = ['colOrd', 'colA', 'colB', 'colC', 'colD']
        inputs ['rowListAsciiA'] = []
        
        inputs['testRowAsciiA'] = ['someData', 100222, 1.00056, 'furtherdata']
        for i in range(1, 10):
            tr = [i] + inputs['testRowAsciiA']
            inputs['rowListAsciiA'].append(tr)

        inputs['rowListAsciiB'] = []
        testRowAsciiB = ['someData', 100223, 1.00057, 'furtherdata']
        for i in range(1, 9):
            tr = [i] + inputs['testRowAsciiA']
            inputs['rowListAsciiB'].append(tr)
        for i in range(9, 10):
            tr = [i] + testRowAsciiB
            inputs['rowListAsciiB'].append(tr)

        inputs['rowListUnicode'] = []
        inputs['testRowUnicode'] = [u'someData', 100222, 1.00056, 
                                    u'abcdÄ†Ä‡ÄˆÄ‰ÄŠÄ‹ÄŒÄ�ÄŽÄ�Ä�Ä‘Ä’Ä“Ä”Ä•Ä–Ä—Ä˜Ä™ÄšÄ›ÄœÄ�ÄžÄŸÄ Ä¡Ä¢Ä£Ä¤Ä¥Ä¦Ä§Ä¨xyz']
        for i in range(1, 10):
            tr = [i] + inputs['testRowUnicode']
            inputs['rowListUnicode'].append(tr)

        inputs['rowListUnicodeMiss'] = []
        inputs['attributeListMiss'] = ['colOrd', 'colA', 'colB', 'colNone', 
                                       'colM1', 'colM2', 'colC', 'colD']
        inputs['testRowUnicodeMiss'] = [u'someData', 100222, None, '?', '.', 
                                        u'abcdÄ†Ä‡ÄˆÄ‰ÄŠÄ‹ÄŒÄ�ÄŽÄ�Ä�Ä‘Ä’Ä“Ä”Ä•Ä–Ä—Ä˜Ä™ÄšÄ›ÄœÄ�ÄžÄŸÄ Ä¡Ä¢Ä£Ä¤Ä¥Ä¦Ä§Ä¨xyz', 
                                        234.2345]
        for i in range(1, 10):
            tr = [i] + inputs['testRowUnicodeMiss']
            inputs['rowListUnicodeMiss'].append(tr)

        return inputs

    @pytest.mark.category_base
    def test_base_basic_ascii(self, category_data):
        dcbA = DataCategoryBase('A', category_data['attributeList'], category_data['rowListAsciiA'])
        dcbB = DataCategoryBase('A', category_data['attributeList'], category_data['rowListAsciiA'])
        assert dcbA == dcbA
        assert dcbB == dcbB
        assert dcbA == dcbB

    @pytest.mark.category_base
    def test_base_methods_ascii(self, category_data):
        name = 'A'
        dcbA = DataCategoryBase(name, category_data['attributeList'], category_data['rowListAsciiA'])
        assert name == dcbA.getName()
        assert category_data['attributeList'] == dcbA.getAttributeList()
        assert category_data['rowListAsciiA'] == dcbA.getRowList()
        assert len(category_data['rowListAsciiA']) == dcbA.getRowCount()
        ii = 0
        dcbA.setMapping('DATA')
        for row in dcbA:
            ii += 1
            assert category_data['testRowAsciiA'] == row[1:]
        assert ii == dcbA.getRowCount()
        dcbA.setMapping('ATTRIBUTE')
        ii = 0
        na = len(dcbA.getAttributeList())
        for row in dcbA:
            ii += 1
            assert ii == row['colOrd']
            assert category_data['testRowAsciiA'][na - 2] == row['colD']

        assert ii == dcbA.getRowCount()
        dcbA.setMapping('ITEM')
        ii = 0
        for row in dcbA:
            ii += 1
            assert ii == row['_' + name + '.' + 'colOrd']
        assert ii == dcbA.getRowCount()

    @pytest.mark.category_base
    def test_base_methods_unicode(self, category_data):
        name = 'A'
        dcbA = DataCategoryBase(name, category_data['attributeList'], category_data['rowListUnicode'])
        assert name == dcbA.getName()
        assert category_data['attributeList'] == dcbA.getAttributeList()
        assert category_data['rowListUnicode'] == dcbA.getRowList()
        assert len(category_data['rowListUnicode']) == dcbA.getRowCount()
        ii = 0
        dcbA.setMapping('DATA')
        for row in dcbA:
            ii += 1
            assert category_data['testRowUnicode'] == row[1:]
        assert ii == dcbA.getRowCount()
        dcbA.setMapping('ATTRIBUTE')
        ii = 0
        na = len(dcbA.getAttributeList())
        for row in dcbA:
            ii += 1
            # logger.info("ii %d row %r " % (ii, row))
            assert ii == row['colOrd']
            assert category_data['testRowUnicode'][na - 2] == row['colD']
            #
        assert ii == dcbA.getRowCount()
        dcbA.setMapping('ITEM')
        ii = 0
        for row in dcbA:
            ii += 1
            assert ii == row['_' + name + '.' + 'colOrd']
            assert category_data['testRowUnicode'][3] == row['_' + name + '.' + 'colD']
        assert ii == dcbA.getRowCount()

    @pytest.mark.category_base
    def test_base_basic_ascii_compare(self, category_data):
        dcbA = DataCategoryBase('A', category_data['attributeList'], category_data['rowListAsciiA'])
        dcbB = DataCategoryBase('A', category_data['attributeList'], category_data['rowListAsciiB'])
        assert dcbA == dcbA
        assert dcbA is dcbA
        assert dcbB == dcbB
        assert dcbA != dcbB
        assert dcbA is not dcbB

    @pytest.mark.category_base
    def test_base_basic_unicode(self, category_data):
        dcbA = DataCategoryBase('A', category_data['attributeList'], category_data['rowListUnicode'])
        dcbB = DataCategoryBase('A', category_data['attributeList'], category_data['rowListUnicode'])
        assert dcbA == dcbA
        assert dcbB == dcbB
        assert dcbA == dcbB

    @pytest.mark.category_subclass
    def test_basic_ascii(self, category_data):
        dcA = DataCategory('A', category_data['attributeList'], category_data['rowListAsciiA'])
        dcB = DataCategory('A', category_data['attributeList'], category_data['rowListAsciiA'])
        assert dcA == dcA
        assert dcB == dcB
        assert dcA == dcB

    @pytest.mark.category_subclass
    def test_basic_ascii_compare(self, category_data):
        dcA = DataCategory('A', category_data['attributeList'], category_data['rowListAsciiA'])
        dcB = DataCategory('A', category_data['attributeList'], category_data['rowListAsciiB'])
        assert dcA == dcA
        assert dcA is dcA
        assert dcB == dcB
        assert dcA != dcB
        assert dcA is not dcB

    @pytest.mark.category_subclass
    def test_basic_unicode(self, category_data):
        dcA = DataCategory('A', category_data['attributeList'], category_data['rowListUnicode'])
        dcB = DataCategory('A', category_data['attributeList'], category_data['rowListUnicode'])
        assert dcA == dcA
        assert dcB == dcB
        assert dcA == dcB

    @pytest.mark.category_subclass
    def test_edit_remove_row(self, category_data):
        dcA = DataCategory('A', category_data['attributeList'], category_data['rowListUnicode'], raiseExceptions=True)
        for jj in range(0, dcA.getRowCount()):
            ii = dcA.getRowCount()
            dcA.removeRow(0)
            assert ii - 1 == dcA.getRowCount()
        #
        assert 0 == dcA.getRowCount()

    @pytest.mark.category_subclass
    def test_edit_row_accessors(self, category_data):
        dcA = DataCategory('A', category_data['attributeList'], category_data['rowListAsciiA'])
        with pytest.raises(IndexError):
            dcA.getRow(dcA.getRowCount() + 1)
        with pytest.raises(IndexError):
            dcA.getRowAttributeDict(dcA.getRowCount() + 1)
        with pytest.raises(IndexError):
            dcA.getRowItemDict(dcA.getRowCount() + 1)

    @pytest.mark.category_subclass
    def test_edit_attributes(self, category_data):
        dcA = DataCategory('A', category_data['attributeList'], category_data['rowListAsciiA'])
        assert 0 == dcA.getRowIndex()
        assert None == dcA.getCurrentAttribute()
        #
        na = len(dcA.getAttributeList())
        tL = dcA.getAttributeListWithOrder()
        assert len(tL) == na

        na = len(dcA.getAttributeList())
        assert dcA.appendAttribute("ColNew") == na + 1
        row = dcA.getFullRow(0)
        assert row[na] == "?"
        #
        row = dcA.getFullRow(dcA.getRowCount() + 1)
        for c in row:
            assert c == "?"
        #

    @pytest.mark.category_subclass
    def test_edit_extend(self, category_data):
        dcA = DataCategory('A', category_data['attributeList'], category_data['rowListAsciiA'])
        na = len(dcA.getAttributeList())
        assert dcA.appendAttributeExtendRows('colNew') == na + 1
        row = dcA.getRow(dcA.getRowCount() - 1)
        assert row[na] == "?"

    @pytest.mark.category_subclass
    def test_get_values(self, category_data):
        dcU = DataCategory('A', category_data['attributeList'], category_data['rowListUnicode'])
        aL = dcU.getAttributeList()
        print("Row length %r " % dcU.getRowCount())
        for ii, v in enumerate(category_data['testRowUnicode']):
            at = aL[ii + 1]
            for j in range(0, dcU.getRowCount()):
                print("ii %d j %d at %s val %r " % (ii, j, at, v))
                assert dcU.getValue(at, j) == v
                assert dcU.getValueOrDefault(at, j, 'mydefault') == v
        #
        # negative indices are interpreted in the python manner
        assert dcU.getValueOrDefault('colOrd', -1, 'default') == 9

        with pytest.raises(IndexError):
            dcU.getValueOrDefault('colOrd', dcU.getRowCount() + 1, 0)
        with pytest.raises(ValueError):
            dcU.getValueOrDefault('badAtt', 0, 0)
        #

    @pytest.mark.category_subclass
    def test_get_select_values(self, category_data):
        dcU = DataCategory('A', category_data['attributeListMiss'], category_data['rowListUnicodeMiss'])
        #
        assert dcU.getFirstValueOrDefault(['colNone', 'colM1', 'colM2', 'colC'], rowIndex=0, defaultValue='default') == u'abcdÄ†Ä‡ÄˆÄ‰ÄŠÄ‹ÄŒÄ�ÄŽÄ�Ä�Ä‘Ä’Ä“Ä”Ä•Ä–Ä—Ä˜Ä™ÄšÄ›ÄœÄ�ÄžÄŸÄ Ä¡Ä¢Ä£Ä¤Ä¥Ä¦Ä§Ä¨xyz'
        assert dcU.getFirstValueOrDefault(['colNone', 'colM1', 'colM2'], rowIndex=0, defaultValue='default') == 'default'

    @pytest.mark.category_subclass
    def test_set_values(self, category_data):
        dcU = DataCategory('A', category_data['attributeListMiss'], category_data['rowListUnicodeMiss'])
        for i in range(0, dcU.getRowCount()):
            dcU.setValue('newValue', attributeName='colM1', rowIndex=i)

        assert dcU.setValue('newValue', attributeName='colM1', rowIndex=dcU.getRowCount() + 5)
        with pytest.raises(ValueError):
            dcU.setValue('newValue', 'colX', 0)

    @pytest.mark.category_subclass
    def test_replace_values(self, category_data):
        dcU = DataCategory('A', category_data['attributeListMiss'], category_data['rowListUnicodeMiss'])
        at = category_data['attributeListMiss'][3]
        curV = category_data['testRowUnicodeMiss'][2]
        assert dcU.replaceValue(curV, 'newVal', at) == dcU.getRowCount()
        at = category_data['attributeListMiss'][4]
        curV = category_data['testRowUnicodeMiss'][3]
        assert dcU.replaceValue(curV, 'newVal', at) == dcU.getRowCount()
        at = category_data['attributeListMiss'][5]
        curV = category_data['testRowUnicodeMiss'][4]
        assert dcU.replaceValue(curV, 'newVal', at) == dcU.getRowCount()

        at = category_data['attributeListMiss'][6]
        curV = category_data['testRowUnicodeMiss'][5]
        assert dcU.replaceValue(curV, 'newVal', at) == dcU.getRowCount()

        for ii in range(3, 7):
            at = category_data['attributeListMiss'][ii]
            assert dcU.replaceSubstring('newVal', 'nextVal', at) == dcU.getRowCount()

    @pytest.mark.category_subclass
    def test_compare_attributes(self, category_data):
        dcU = DataCategory('A', category_data['attributeList'], category_data['rowListUnicode'])
        dcM = DataCategory('A', category_data['attributeListMiss'], category_data['rowListUnicodeMiss'])
        na = len(dcU.getAttributeList())
        t1, t2, t3 = dcU.cmpAttributeNames(dcU)
        assert len(t1) == 0
        assert len(t3) == 0
        assert len(t2) == na
        t1, t2, t3 = dcU.cmpAttributeNames(dcM)
        assert len(t1) == 0
        assert len(t3) == 3
        assert len(t2) == na

    @pytest.mark.category_subclass
    def test_compare_values(self, category_data):
        dcU = DataCategory('A', category_data['attributeList'], category_data['rowListUnicode'])
        dcM = DataCategory('A', category_data['attributeListMiss'], category_data['rowListUnicodeMiss'])
        na = dcU.getAttributeList()
        assert len(na) >= 1
        tupL = dcU.cmpAttributeValues(dcU)
        for tup in tupL:
            assert tup[1] == True
        tupL = dcU.cmpAttributeValues(dcM)
        for tup in tupL:
            if tup[0] in ['colC', 'colD']:
                assert tup[1] == False
            else:
                assert tup[1] == True
        #
        dcX = DataCategory('A', category_data['attributeList'], category_data['rowListUnicode'])
        assert dcX.setValue(u'134Ä†Ä‡ÄˆÄ‰ÄŠÄ‹ÄŒÄ�ÄŽÄ�Ä�Ä‘Ä’Ä“Ä Ä¡Ä¢Ä£Ä¤Ä¥Ä¦Ä§Ä¨xyz', attributeName='colD', rowIndex=dcX.getRowCount() - 2)
        tupL = dcU.cmpAttributeValues(dcX)
        for tup in tupL:
            if tup[0] in ['colD']:
                assert tup[1] == False
            else:
                assert tup[1] == True

    @pytest.mark.category_subclass
    def test_cond_select_values(self, category_data):
        dcM = DataCategory('A', category_data['attributeListMiss'], category_data['rowListUnicodeMiss'])
        atL = dcM.getAttributeList()
        for ii, at in enumerate(atL[1:]):
            assert len(dcM.selectIndices(category_data['testRowUnicodeMiss'][ii], at)) == dcM.getRowCount()
        #
        print("Window %r" % [tt for tt in window(atL)])
        for atW in window(atL, size=1):
            assert len(dcM.selectValueListWhere(atW, category_data['testRowUnicodeMiss'][-1], category_data['attributeListMiss'][-1])) == dcM.getRowCount()
        for atW in window(atL, size=2):
            assert len(dcM.selectValueListWhere(atW, category_data['testRowUnicodeMiss'][-1], category_data['attributeListMiss'][-1])) == dcM.getRowCount()
        for atW in window(atL, size=3):
            assert len(dcM.selectValueListWhere(atW, category_data['testRowUnicodeMiss'][-1], category_data['attributeListMiss'][-1])) == dcM.getRowCount()
        for atW in window(atL, size=4):
            assert len(dcM.selectValueListWhere(atW, category_data['testRowUnicodeMiss'][-1], category_data['attributeListMiss'][-1])) == dcM.getRowCount()


