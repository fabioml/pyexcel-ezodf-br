'''
Created on Nov 20, 2023

@author: fabio
'''
import unittest
from ezodf.named import NamedExpressions
from lxml import etree
from lxml.etree import _Element
from ezodf.xmlns import wrap, CN, subelement
from ezodf.table import Table



NAMEDSEXP1 = """
<ns0:named-expressions xmlns:ns0="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
    <ns0:named-range ns0:cell-range-address="$SHEET1.$A$2" ns0:base-cell-address="$SHEET1.$A$2" ns0:name="XXX"/>
</ns0:named-expressions>
"""
NAMEDSEXP2 = """
<ns0:named-expressions xmlns:ns0="urn:oasis:names:tc:opendocument:xmlns:table:1.0">
    <ns0:named-range ns0:cell-range-address="$SHEET1.$A$2" ns0:base-cell-address="$SHEET1.$A$2" ns0:name="XXX"/>
    <ns0:named-range ns0:cell-range-address="$SHEET1.$B$1" ns0:base-cell-address="$SHEET1.$B$1" ns0:name="YYY"/>
</ns0:named-expressions>
"""

class Test(unittest.TestCase):
    parser = etree.XMLParser(remove_blank_text=True)
                             # recover=True)
    
    def normalizeXML(self, expect,xml):
        obj1 = expect
        obj2 = xml
        if not isinstance(expect, _Element):
            obj1 = etree.XML(expect.encode('utf-8'),self.parser)
        if not isinstance(xml, _Element):
            obj2 = etree.XML(xml.encode('utf-8'),self.parser)
        expect = etree.tostring(obj1,
                                xml_declaration=True,
                                encoding='UTF-8')
        result = etree.tostring(obj2,
                                xml_declaration=True,
                                encoding='UTF-8')
        self.assertEqual(expect, result,"\n{}\n{}".format(expect,result))
        

    def test_oneNamed(self):
        named = NamedExpressions()
        named.add_named("SHEET1", "XXX", "A2")
        self.normalizeXML(NAMEDSEXP1,named.xmlnode)
        
    def test_twoNamed(self):
        named = NamedExpressions()
        named.add_named("SHEET1", "XXX", "A2")
        named.add_named("SHEET1", "YYY", "B1")
        self.normalizeXML(NAMEDSEXP2,named.xmlnode)
        
    def test_twoSameName(self):
        named = NamedExpressions()
        named.add_named("SHEET1", "XXX", "B1")
        named.add_named("SHEET1", "XXX", "A2")
        self.normalizeXML(NAMEDSEXP1,named.xmlnode)
    
    def test_twoNamedRemoveOne(self):
        named = NamedExpressions()
        named.add_named("SHEET1", "XXX", "A2")
        named.add_named("SHEET1", "YYY", "B1")
        named.del_named("YYY")
        self.normalizeXML(NAMEDSEXP1,named.xmlnode)
    
    def test_removeException(self):
        named = NamedExpressions()
        with self.assertRaisesRegex(KeyError, "Unable to find: XXX"):
            named.del_named("XXX")
    
    def test_twoNamedByIndex(self):
        named = NamedExpressions()
        named.add_named("SHEET1", "XXX", (1,0))
        named.add_named("SHEET1", "YYY", (0,1))
        self.normalizeXML(NAMEDSEXP2,named.xmlnode)
        
    def test_usingTableName(self):
        sheet = Table()
        sheet.name ="SHEET1"
        named = NamedExpressions()
        named.add_named(sheet, "XXX", (1,0))
        self.normalizeXML(NAMEDSEXP1,named.xmlnode)
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()