##
# File:      Method.py
# Orignal:   Aug 12, 2013   Jdw
#
# Updates:
#   01-Aug-2017   jdw migrate portions to public repo
#   12-Jun-2018   jdw add missing accessor for MethodDefinition getCode()
#    9-Sep-2018   jdw add priority to method definition
#
##
"""
Utility classes for applying dictionary methods on PDBx/mmCIF data files.
"""

from __future__ import absolute_import

import sys

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"


class MethodDefinition(object):

    def __init__(self, method_id, code='calculate', language='Python', inline=None, priority=None):
        self.method_id = method_id
        self.language = language
        self.code = code
        self.inline = inline
        self.priority = priority if priority else 1

    def getId(self):
        return self.method_id

    def getLanguage(self):
        return self.language

    def getCode(self):
        return self.code

    def getInline(self):
        return self.inline

    def getPriority(self):
        return self.priority

    def printIt(self, fh=sys.stdout):
        fh.write("------------- Method definition -------------\n")
        fh.write("Id:           %s\n" % self.method_id)
        fh.write("Code:         %s\n" % self.code)
        fh.write("Language:     %s\n" % str(self.language))
        fh.write("Inline text:  %s\n" % str(self.inline))
        fh.write("Priority:     %d\n" % self.priority)


class MethodReference(object):

    def __init__(self, method_id, type='attribute', category=None, attribute=None):
        self.method_id = method_id
        self.type = type
        self.categoryName = category
        self.attributeName = attribute

    def getId(self):
        return self.method_id

    def getType(self):
        return self.type

    def getCategoryName(self):
        return self.categoryName

    def getAttributeName(self):
        return self.attributeName

    def printIt(self, fh=sys.stdout):
        fh.write("--------------- Method Reference -----------------\n")
        fh.write("Id:             %s\n" % self.method_id)
        fh.write("Type:           %s\n" % self.type)
        fh.write("Category name:  %s\n" % str(self.categoryName))
        fh.write("Attribute name: %s\n" % str(self.attributeName))
