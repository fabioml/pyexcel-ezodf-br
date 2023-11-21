#!/usr/bin/env python
#coding:utf-8
# Purpose: ODF styles.xml document management
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
from ezodf.xmlns import subelementMoreThanOne
__author__ = "mozman <mozman@gmx.at>"

from .const import STYLES_NSMAP
from .xmlns import XMLMixin, subelement, etree, CN, register_class, wrap
from .base import GenericWrapper

## file 'styles.xml'

@register_class
class OfficeDocumentStyles(XMLMixin):
    TAG = CN('office:document-styles')

    def __init__(self, xmlnode=None):
        if xmlnode is None:
            self.xmlnode = etree.Element(self.TAG, nsmap=STYLES_NSMAP)
        elif xmlnode.tag == self.TAG:
            self.xmlnode = xmlnode
        else:
            raise ValueError("Unexpected root node: %s" % content.tag)
        self._setup()

    def _setup(self):
        self.fonts = wrap(subelement(self.xmlnode, CN('office:font-face-decls')))
        self.styles = wrap(subelement(self.xmlnode, CN('office:styles')))
        self.automatic_styles = wrap(subelement(self.xmlnode, CN('office:automatic-styles')))
        self.master_styles = wrap(subelement(self.xmlnode, CN('office:master-styles')))

## style container

class Container(object):
    def __init__(self, xmlnode):
        assert xmlnode.tag == self.TAG
        self.xmlnode = xmlnode
        self._cache = {}

    def __getitem__(self, key):
        style = self._find(key) # by style:name attribute
        if style is not None:
            return wrap(style)
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        style = self._find(key)
        if style is None:
            self.xmlnode.append(value.xmlnode)
        else:
            self.xmlnode.replace(style, value.xmlnode)
        self._cache[key] = value

    def _find(self, name):
        try:
            return self._cache[name]
        except KeyError:
            for style in self.xmlnode.iterchildren():
                stylename = style.get(CN('style:name'))
                if stylename == name:
                    self._cache[name] = style
                    return style
        return None

@register_class
class OfficeFontFaceDecls(Container):
    TAG = CN('office:font-face-decls')

    
@register_class
class OfficeStyles(Container):
    TAG = CN('office:styles')
        
@register_class
class OfficeMasterStyles(Container):
    TAG = CN('office:master-styles')

## style objects


class BaseStyle(GenericWrapper):
    ATTRIBUTEMAP = {}

    def __init__(self, xmlnode):
        self.xmlnode = xmlnode

    def __getitem__(self, key):
        """ Get style attribute 'key'. """
        return self.get_attr(self.ATTRIBUTEMAP[key])

    def __setitem__(self, key, value):
        self.set_attr(self.ATTRIBUTEMAP[key], value)

    def _properties(self, key, property_factory, new=True):
        """ Get or create a properties element. """
        element = subelement(self.xmlnode, key , new)
        if element is None:
            raise KeyError(key)
        propertiesname = key + '-properties'
        properties = element.find(propertiesname)
        if properties is None:
            properties = etree.SubElement(element, propertiesname)
        return property_factory(properties)
        
class Properties(BaseStyle):
    ATTRIBUTEMAP = {} # should contain all possible property names
    pass

HeaderProperties = Properties

@register_class
class Style(BaseStyle):
    TAG = CN('style:style')
    ATTRIBUTEMAP = {
        'name': CN('style:name'),
        'display-name': CN('style:display-name'),
        'family': CN('style:family'),
        'parent-style-name': CN('style:parent-style-name'),
        'next-style-name': CN('style:next-style-name'),
        'list-style-name': CN('style:list-style-name'),
        'master-page-name': CN('style:master-page-name'),
        'auto-update': CN('style:auto-update'), # 'true' or 'false'
        'data-style-name': CN('style:data-style-name'),
        'class': CN('style:class'),
        'default-outline-level': CN('style:default-outline-level'),
    }
    
@register_class
class DefaultStyle(BaseStyle):
    TAG = CN('style:default-style')
    ATTRIBUTEMAP = {
        'family': CN('style:family'),
    }

@register_class
class PageLayout(BaseStyle):
    TAG = CN('style:page-layout')
    ATTRIBUTEMAP = {
        'name': CN('style:name'),
        'page-usage': CN('style:page-usage'), # all | left | right | mirrored
    }
    def __init__(self, xmlelement):
        super(PageLayout, self).__init__(xmlelement)
        self.header = self._properties(CN('style:header-style'), HeaderProperties)
        self.footer = self._properties(CN('style:footer-style'), HeaderProperties)

@register_class
class FontFace(BaseStyle):
    TAG = CN('style:font-face')


@register_class
class NumberNumber(BaseStyle):
    TAG = CN('number:number')
    ATTRIBUTEMAP = {
        'decimal-places': CN('number:decimal-places'),
        'min-decimal-places': CN('number:min-decimal-places'),
        'min-integer-digits': CN('number:min-integer-digits'),
        'grouping': CN('number:grouping'),
    }

@register_class
class NumberText(BaseStyle):
    TAG = CN('number:text')
    def __init__(self, xmlnode=None):
        super(NumberText, self).__init__(xmlnode=xmlnode)

@register_class
class NumberCurrencySymbol(BaseStyle):
    TAG = CN('number:currency-symbol')
    ATTRIBUTEMAP = {
        'language': CN('number:language'),
        'country': CN('number:country')
    }
    def __init__(self, xmlnode=None):
        super(NumberCurrencySymbol, self).__init__(xmlnode=xmlnode)

@register_class
class StyleTextProperties(BaseStyle):
    TAG = CN('style:text-properties')    
    ATTRIBUTEMAP = {
        'color': CN('fo:color')
    }
@register_class
class StyleMap(BaseStyle):
    TAG = CN('style:map')    
    ATTRIBUTEMAP = {
        'condition': CN('style:condition'),
        'apply-style-name': CN('style:apply-style-name'),
    }   

@register_class
class NumberCurrencyStyle(BaseStyle):
    TAG = CN('number:currency-style')
    
    ATTRIBUTEMAP = {
        'name': CN('style:name')
    }
    def __init__(self, xmlnode=None):
        super(NumberCurrencyStyle, self).__init__(xmlnode=xmlnode)
    def positive(self, name):
        self['name']=name
        self.symbol = wrap(subelementMoreThanOne(self.xmlnode, CN('number:currency-symbol')))
        self.symbol['language']= 'pt'
        self.symbol['country']= 'BR'
        self.symbol.text = "R$"
        self.ntext2 = wrap(subelementMoreThanOne(self.xmlnode, CN('number:text')))
        self.ntext2.text = " "
        self.n1 = wrap(subelementMoreThanOne(self.xmlnode, CN('number:number')))
        self.n1['decimal-places']='2'
        self.n1['min-decimal-places']='2'
        self.n1['min-integer-digits']='1'
        self.n1['grouping']='true'        
    def negative(self, name, positiveName):
        self.ntextColor = wrap(subelementMoreThanOne(self.xmlnode, CN('style:text-properties')))
        self.ntextColor['color']='#ff0000'
        self.ntextNeg = wrap(subelementMoreThanOne(self.xmlnode, CN('number:text')))
        self.ntextNeg.text = "-"
        self.positive(name)
        self.conditionMap = wrap(subelementMoreThanOne(self.xmlnode, CN('style:map')))
        self.conditionMap['condition']='value()>=0'
        self.conditionMap['apply-style-name']=positiveName
        
        
@register_class
class NumberStyle(BaseStyle):
    TAG = CN('number:number-style')
    
    ATTRIBUTEMAP = {
        'name': CN('style:name')
    }
    def __init__(self, xmlnode=None):
        super(NumberStyle, self).__init__(xmlnode=xmlnode)
        self.n1 = wrap(subelement(self.xmlnode, CN('number:number')))
        self.n1['decimal-places']='2'
        self.n1['min-decimal-places']='2'
        self.n1['min-integer-digits']='1'
            
        
@register_class
class OfficeAutomaticStyles(GenericWrapper):
    TAG = CN('office:automatic-styles')
    def __init__(self, xmlnode=None):
        super(OfficeAutomaticStyles, self).__init__(xmlnode=xmlnode)
    def default_content(self):
        self.floatStyleNumber = wrap(subelementMoreThanOne(self.xmlnode, CN('number:number-style')))
        self.floatStyleNumber['name']='floatStyle'
        self.floatStyleStyle = wrap(subelementMoreThanOne(self.xmlnode, CN('style:style')))
        self.floatStyleStyle['name']='floatStyle'
        self.fillDefaultStyle(self.floatStyleStyle, self.floatStyleNumber['name'])
        
        etree.Element(self.TAG, nsmap=STYLES_NSMAP)
        
        self.currencyStyleNumberPositive = wrap(subelementMoreThanOne(self.xmlnode, CN('number:currency-style')))
        self.currencyStyleNumberPositive.positive('currencyStylePositive')
        self.currencyStyleNumberNegative = wrap(subelementMoreThanOne(self.xmlnode, CN('number:currency-style')))
        self.currencyStyleNumberNegative.negative('currencyStyle','currencyStylePositive')
        self.currencyStyleStyle = wrap(subelementMoreThanOne(self.xmlnode, CN('style:style'), True))
        self.currencyStyleStyle['name']='currencyStyle'
        self.fillDefaultStyle(self.currencyStyleStyle, self.currencyStyleNumberNegative['name'])
        
    def fillDefaultStyle(self, styleElem, associateName):
        styleElem['parent-style-name']='Default'
        styleElem['family']='table-cell'
        styleElem['data-style-name']=associateName