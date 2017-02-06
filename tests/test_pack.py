# -*- coding: utf-8 -*-
import mock
import random
import unittest

from mayaqua import Buf
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
        value = random.randint(1, 1000000)
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

    def test_write_element(self):
        buf = mock.MagicMock()
        tup = 'SomeName', 'SomeValue'
        buf.write_name = mock.MagicMock()
        buf.write_int = mock.MagicMock()
        buf.write_value = mock.MagicMock()
        Pack.write_element(buf, tup)
        buf.write_name.assert_called_once_with(tup[0])
        buf.write_int.assert_has_calls(calls=[mock.call(Buf.get_type(tup[1])), mock.call(1)], any_order=True)
        buf.write_value.assert_called_once_with(tup[1])

    def test_read_element(self):
        value_type = 123
        name = 'name'
        value = 'value'
        buf = mock.MagicMock()
        buf.read_name = mock.MagicMock(return_value=name)
        buf.read_int = mock.MagicMock(return_value=value_type)
        buf.read_value = mock.MagicMock(return_value=value)
        result = Pack.read_element(buf)
        buf.read_name.assert_called_once()
        buf.read_int.assert_called()
        buf.read_value.assert_called_with(value_type)
        self.assertEqual(result, (name, value))
