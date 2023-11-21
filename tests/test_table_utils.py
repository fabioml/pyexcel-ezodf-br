#!/usr/bin/env python
#coding:utf-8
# Purpose: test table utils
# Created: 13.02.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT license
from __future__ import unicode_literals, print_function, division
__author__ = "mozman <mozman@gmx.at>"

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from ezodf.tableutils import address_to_index, iter_cell_range, index_to_address

class TestAddressToIndex(unittest.TestCase):
    def test_A1(self):
        self.assertEqual(address_to_index('A1'), (0, 0))

    def test_lowercase_a1(self):
        self.assertEqual(address_to_index('a1'), (0, 0))

    def test_A2(self):
        self.assertEqual(address_to_index('A2'), (1, 0))

    def test_C2(self):
        self.assertEqual(address_to_index('C2'), (1, 2))

    def test_AB2(self):
        self.assertEqual(address_to_index('AB2'), (1, 27))
        self.assertEqual(address_to_index('BB2'), (1, 53))
        self.assertEqual(address_to_index('BCD1'), (0, 1433))
        self.assertEqual(address_to_index('BCE1'), (0, 1434))
        self.assertEqual(address_to_index('AAA2'), (1, 702))
        self.assertEqual(address_to_index('CC2'), (1, 80))
        
    def test_ABC2(self):
        self.assertEqual(address_to_index('ABC2'), (1, 730))

    def test_AA100(self):
        self.assertEqual(address_to_index('AA100'), (99, 26))

    def test_CCC100(self):
        self.assertEqual(address_to_index('CCC100'), (99, 2108))

    def test_errors(self):
        with self.assertRaises(ValueError):
            address_to_index('100')
        with self.assertRaises(ValueError):
            address_to_index('A')
        with self.assertRaises(ValueError):
            address_to_index('A1A')

class TestIterCellRange(unittest.TestCase):
    def test_range(self):
        result = list(iter_cell_range((0,0), (2, 2)))
        self.assertEqual(4, len(result))
        self.assertListEqual([(0,0), (0,1), (1, 0), (1, 1)], result)

    def test_size_error_negative_rows(self):
        with self.assertRaises(ValueError):
            list(iter_cell_range((0, 0), (-1, 1)))

    def test_size_error_negative_columns(self):
        with self.assertRaises(ValueError):
            list(iter_cell_range((0, 0), (1, -1)))

    def test_size_error_zero_rows(self):
        with self.assertRaises(ValueError):
            list(iter_cell_range((0, 0), (0, 1)))

    def test_size_error_zero_columns(self):
        with self.assertRaises(ValueError):
            list(iter_cell_range((0, 0), (1, 0)))

    def test_pos_error_negative_start_row(self):
        with self.assertRaises(ValueError):
            list(iter_cell_range((-1, 0), (1, 1)))

    def test_pos_error_negative_start_column(self):
        with self.assertRaises(ValueError):
            list(iter_cell_range((0, -1), (1, 1)))

class TestIndexToAddress(unittest.TestCase):
    def test_A1(self):
        self.assertEqual(index_to_address((0, 0)), 'A1')

    def test_A2(self):
        self.assertEqual(index_to_address((1, 0)), 'A2')
    
    def test_C2(self):
        self.assertEqual(index_to_address((1, 2)), 'C2')

    def test_AA2(self):
        self.assertEqual(index_to_address((1, 27)), 'AB2')
        self.assertEqual(index_to_address((1, 27)), 'AB2')
        self.assertEqual(index_to_address((1, 53)), 'BB2')
        self.assertEqual(index_to_address((0, 1433)), 'BCD1')
        self.assertEqual(index_to_address((0, 1434)), 'BCE1')
        self.assertEqual(index_to_address((1, 702)), 'AAA2')
        self.assertEqual(index_to_address((1, 80)), 'CC2')
    
    def test_AA100(self):
        self.assertEqual(index_to_address((99, 26)), 'AA100')
    
    def test_CCC100(self):
        self.assertEqual(index_to_address((99, 2108)), 'CCC100')
    
    def test_errors(self):
        with self.assertRaises(TypeError):
            index_to_address('100')


if __name__=='__main__':
    unittest.main()
