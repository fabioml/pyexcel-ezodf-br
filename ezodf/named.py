'''
Created on Nov 17, 2023

@author: fabio
'''
from ezodf.xmlns import CN, wrap, register_class, subelementMoreThanOne
from ezodf.base import GenericWrapper
from ezodf.propertymixins import StringProperty
from ezodf.table import Table
from ezodf.cells import Cell
from ezodf.tableutils import CELL_ADDRESS, index_to_address

@register_class
class NamedRange(GenericWrapper):
    TAG = CN('table:named-range')
    tableName = StringProperty(CN('table:name'))
    cellRangeAddress = StringProperty(CN('table:cell-range-address'))
    baseCellAddress = StringProperty(CN('table:base-cell-address'))
    
    def __init__(self, xmlnode=None):
        super(NamedRange, self).__init__(xmlnode=xmlnode)
    
@register_class
class NamedExpressions(GenericWrapper):
    TAG = CN('table:named-expressions')
    
    def __init__(self, xmlnode=None):
        super(NamedExpressions, self).__init__(xmlnode=xmlnode)
        self.ranges={}
    
    def add_named(self, sheet, name, namedRange):
        sheetName = sheet
        if isinstance(sheet, Table):
            sheetName =sheet.name
        if isinstance(namedRange,tuple):
            namedRange = index_to_address(namedRange) 
        res = CELL_ADDRESS.match(namedRange.upper())
        if not res:
            raise ValueError('Invalid cell address: %s' % namedRange)
        column_name, row_name = res.groups()
        namedRange="${}.${}${}".format(sheetName ,column_name, row_name)
        if name in self.ranges:
            self.xmlnode.remove(self.ranges[name].xmlnode)
        self.ranges[name]=wrap(subelementMoreThanOne(self.xmlnode, CN('table:named-range')))
        self.ranges[name].cellRangeAddress=namedRange
        self.ranges[name].baseCellAddress=namedRange
        self.ranges[name].tableName = name
    
    def del_named(self, name):
        if name in self.ranges:
            self.xmlnode.remove(self.ranges[name].xmlnode)
        else:
            raise KeyError('Unable to find: %s' % name) 
        
    
    
    
    

        