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
        self.del_named(name, False)
        namedCreated =wrap(subelementMoreThanOne(self.xmlnode, CN('table:named-range')))
        namedCreated.cellRangeAddress=namedRange
        namedCreated.baseCellAddress=namedRange
        namedCreated.tableName = name
    
    def del_named(self, name, exceptionNotFound = True):
        for n in  self.xmlnode.findall(NamedRange.TAG):
            w = wrap(n)
            if w.tableName == name:
                self.xmlnode.remove(n)
                return
        if exceptionNotFound:
            raise KeyError('Unable to find: %s' % name) 
        
    
    
    
    

        