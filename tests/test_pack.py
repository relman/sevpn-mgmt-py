# -*- coding: utf-8 -*-
from random import randint as rint
import unittest

from mayaqua import Pack


class TestPack(unittest.TestCase):
    def test_add_value_bool(self):
        name = 'BoolVal'
        value = True
        p = Pack()
        p.add_value(name, value)
        self.assertEqual(len(p._pack), 1)
        self.assertEqual(p._pack[name], value is True)

    def test_add_value_int(self):
        name = 'IntVal'
        value = rint(1, 1000000)
        p = Pack()
        p.add_value(name, value)
        self.assertEqual(len(p._pack), 1)
        self.assertEqual(p._pack[name], value)

    def test_add_value_str(self):
        name = 'StrVal'
        value = 'some string value'
        p = Pack()
        p.add_value(name, value)
        self.assertEqual(len(p._pack), 1)
        self.assertEqual(p._pack[name], value)

    def test_add_value_bytearray(self):
        name = 'DataVal'
        value = bytearray('123')
        p = Pack()
        p.add_value(name, value)
        self.assertEqual(len(p._pack), 1)
        self.assertEqual(p._pack[name], value)

    def test_add_value_unicode(self):
        name = 'UniVal'
        value = u'Unicode string ¤„©'
        p = Pack()
        p.add_value(name, value)
        self.assertEqual(len(p._pack), 1)
        self.assertEqual(p._pack[name], value)

    def test_add_value_long(self):
        name = 'LongVal'
        value = 9876543210L
        p = Pack()
        p.add_value(name, value)
        self.assertEqual(len(p._pack), 1)
        self.assertEqual(p._pack[name], value)

    def test_add_value_exception(self):
        name = 'Exception'
        value = OSError()
        p = Pack()
        with self.assertRaises(Exception):
            p.add_value(name, value)

    def test_create_dummy_value(self):
        name = 'pencore'
        p = Pack()
        p.create_dummy_value()
        self.assertEqual(len(p._pack), 1)
        self.assertTrue(name in p._pack)
        self.assertTrue(len(p._pack[name]) < p.HTTP_PACK_RAND_SIZE_MAX)
