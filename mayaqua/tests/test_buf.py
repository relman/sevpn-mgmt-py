# -*- coding: utf-8 -*-
import mock
import unittest

from mayaqua import Buf


class TestBuf(unittest.TestCase):
    def test_len(self):
        val = bytearray('1234\x00\xff')
        buf = Buf(val)
        self.assertEqual(len(buf), len(val))

    def test_get_type_bool(self):
        val = True
        expected = Buf.TYPE_INT
        result = Buf.get_type(val)
        self.assertEqual(result, expected)

    def test_get_type_int(self):
        val = 123
        expected = Buf.TYPE_INT
        result = Buf.get_type(val)
        self.assertEqual(result, expected)

    def test_get_type_data(self):
        val = bytearray('some data')
        expected = Buf.TYPE_DATA
        result = Buf.get_type(val)
        self.assertEqual(result, expected)

    def test_get_type_str(self):
        val = 'some string here'
        expected = Buf.TYPE_STR
        result = Buf.get_type(val)
        self.assertEqual(result, expected)

    def test_get_type_unicode(self):
        val = u'Testing «ταБЬℓσ»: 1<2 & 4+1>3'
        expected = Buf.TYPE_UNISTR
        result = Buf.get_type(val)
        self.assertEqual(result, expected)

    def test_get_type_int64(self):
        val = 9876543210L
        expected = Buf.TYPE_UINT64
        result = Buf.get_type(val)
        self.assertEqual(result, expected)

    def test_int_to_bytes(self):
        value = 1
        expected = '\x00\x00\x00\x01' if Buf.is_little() else '\x01\x00\x00\x00'
        result = Buf.int_to_bytes(value)
        self.assertEqual(result, expected)

    def test_bytes_to_int(self):
        value = bytearray('\x00\x00\x00\x02') if Buf.is_little() else '\x02\x00\x00\x00'
        expected = 2
        result = Buf.bytes_to_int(value)
        self.assertEqual(result, expected)

    def test_write_int(self):
        val = 0xaf88cb99
        expected = '\xaf\x88\xcb\x99' if Buf.is_little() else '\x99\xcb\x88\xaf'
        buf = Buf()
        buf.write_int(val)
        self.assertEqual(buf.storage, expected)

    def test_write_data(self):
        value = bytearray('abcdef')
        expected = '\x00\x00\x00\x06abcdef' if Buf.is_little() else '\x06\x00\x00\x00abcdef'
        buf = Buf()
        buf.write_data(value)
        self.assertEqual(buf.storage, expected)

    def test_write_name(self):
        value = 'new string'
        expected = '\x00\x00\x00\x0bnew string' if Buf.is_little() else '\x0b\x00\x00\x00new string'
        buf = Buf()
        buf.write_name(value)
        self.assertEqual(buf.storage, expected)

    def test_write_str(self):
        value = 'new string'
        expected = '\x00\x00\x00\nnew string' if Buf.is_little() else '\n\x00\x00\x00new string'
        buf = Buf()
        buf.write_str(value)
        self.assertEqual(buf.storage, expected)

    def test_write_str_unicode(self):
        value = u'Testing «ταБЬℓσ»: 1<2 & 4+1>3'
        expected = (
            '\x00\x00\x00&Testing '
            '\xc2\xab\xcf\x84\xce\xb1\xd0\x91\xd0\xac\xe2\x84\x93\xcf\x83\xc2\xbb: 1<2 & 4+1>3'
        ) if Buf.is_little() else (
            '&\x00\x00\x00Testing '
            '\xc2\xab\xcf\x84\xce\xb1\xd0\x91\xd0\xac\xe2\x84\x93\xcf\x83\xc2\xbb: 1<2 & 4+1>3'
        )
        buf = Buf()
        buf.write_str_unicode(value)
        self.assertEqual(buf.storage, expected)

    def test_write_int64(self):
        val = 0xab88cd99ef11aa
        expected = '\x00\xab\x88\xcd\x99\xef\x11\xaa' if Buf.is_little() else '\xaa\x11\xef\x99\xcd\x88\xab\x00'
        buf = Buf()
        buf.write_int64(val)
        self.assertEqual(buf.storage, expected)

    def test_write_value_none(self):
        value = None
        buf = Buf()
        buf.get_type = mock.MagicMock()
        buf.write_value(value)
        buf.get_type.assert_not_called()

    def test_write_value_int(self):
        value = 123
        val_type = Buf.TYPE_INT
        buf = Buf()
        Buf.get_type = mock.MagicMock(return_value=val_type)
        buf.write_int = mock.MagicMock()
        buf.write_value(value)
        Buf.get_type.assert_called_with(value)
        buf.write_int.assert_called_with(value)

    def test_write_value_data(self):
        value = bytearray('123')
        val_type = Buf.TYPE_DATA
        buf = Buf()
        Buf.get_type = mock.MagicMock(return_value=val_type)
        buf.write_data = mock.MagicMock()
        buf.write_value(value)
        Buf.get_type.assert_called_with(value)
        buf.write_data.assert_called_with(value)

    def test_write_value_str(self):
        value = 'string'
        val_type = Buf.TYPE_STR
        buf = Buf()
        Buf.get_type = mock.MagicMock(return_value=val_type)
        buf.write_str = mock.MagicMock()
        buf.write_value(value)
        Buf.get_type.assert_called_with(value)
        buf.write_str.assert_called_with(value)

    def test_write_value_unicode(self):
        value = u'string ®'
        val_type = Buf.TYPE_UNISTR
        buf = Buf()
        Buf.get_type = mock.MagicMock(return_value=val_type)
        buf.write_str_unicode = mock.MagicMock()
        buf.write_value(value)
        Buf.get_type.assert_called_with(value)
        buf.write_str_unicode.assert_called_with(value)

    def test_write_value_int64(self):
        value = 9876543210L
        val_type = Buf.TYPE_UINT64
        buf = Buf()
        Buf.get_type = mock.MagicMock(return_value=val_type)
        buf.write_int64 = mock.MagicMock()
        buf.write_value(value)
        Buf.get_type.assert_called_with(value)
        buf.write_int64.assert_called_with(value)

    def test_read_bytes(self):
        value = bytearray('1234 example')
        expected = bytearray('1234 ')
        expected_offset = len(expected)
        size = 5
        buf = Buf(value)
        result = buf.read_bytes(size)
        self.assertEqual(result, expected)
        self.assertEqual(buf.offset, expected_offset)

    def test_read_int(self):
        value = bytearray('\x00\x00\x00\x0ctest 123456') if Buf.is_little() \
            else bytearray('\x0c\x00\x00\x00test 123456')
        expected = 0x0c
        expected_offset = 4
        buf = Buf(value)
        result = buf.read_int()
        self.assertEqual(result, expected)
        self.assertEqual(buf.offset, expected_offset)

    def test_read_data(self):
        value = bytearray('\x00\x00\x00\x08new test12345678') if Buf.is_little() \
            else bytearray('\x08\x00\x00\x00new test12345678')
        expected = 'new test'
        expected_offset = 12
        buf = Buf(value)
        result = buf.read_data()
        self.assertEqual(result, expected)
        self.assertEqual(buf.offset, expected_offset)

    def test_read_name(self):
        value = bytearray('\x00\x00\x00\x0bnew string\x00321654\x00test data 123456789') if Buf.is_little() \
            else bytearray('\x0b\x00\x00\x00new string\x00321654\x00test data 123456789')
        expected = 'new string'
        expected_offset = 14
        buf = Buf(value)
        result = buf.read_name()
        self.assertEqual(result, expected)
        self.assertEqual(buf.offset, expected_offset)

    def test_read_str(self):
        value = bytearray('\x00\x00\x00\x0anew string\x00321654\x00test data 123456789') if Buf.is_little() \
            else bytearray('\x0a\x00\x00\x00new string\x00321654\x00test data 123456789')
        expected = 'new string'
        expected_offset = 14
        buf = Buf(value)
        result = buf.read_str()
        self.assertEqual(result, expected)
        self.assertEqual(buf.offset, expected_offset)

    def test_read_str_unicode(self):
        value = bytearray(
            '\x00\x00\x00&Testing '
            '\xc2\xab\xcf\x84\xce\xb1\xd0\x91\xd0\xac\xe2\x84\x93\xcf\x83\xc2\xbb: 1<2 & 4+1>3\x00'
        ) if Buf.is_little() else bytearray(
            '&\x00\x00\x00Testing '
            '\xc2\xab\xcf\x84\xce\xb1\xd0\x91\xd0\xac\xe2\x84\x93\xcf\x83\xc2\xbb: 1<2 & 4+1>3\x00'
        )
        expected = u'Testing «ταБЬℓσ»: 1<2 & 4+1>3'
        expected_offset = 42
        buf = Buf(value)
        result = buf.read_str_unicode()
        self.assertEqual(result, expected)
        self.assertEqual(buf.offset, expected_offset)

    def test_read_int64(self):
        value = '\x00\xab\x88\xcd\x99\xef\x11\xaa' if Buf.is_little() else '\xaa\x11\xef\x99\xcd\x88\xab\x00'
        expected = 0xab88cd99ef11aa
        buf = Buf(value)
        result = buf.read_int64()
        self.assertEqual(result, expected)

    def test_read_value_none(self):
        t = Buf.TYPE_UNKNOWN
        expected = None
        buf = Buf()
        result = buf.read_value(t)
        self.assertEqual(result, expected)

    def test_read_value_int(self):
        t = Buf.TYPE_INT
        expected = 123
        buf = Buf()
        buf.read_int = mock.MagicMock(return_value=expected)
        result = buf.read_value(t)
        self.assertEqual(result, expected)
        buf.read_int.assert_called_once()

    def test_read_value_data(self):
        t = Buf.TYPE_DATA
        expected = bytearray('\x01\x02')
        buf = Buf()
        buf.read_data = mock.MagicMock(return_value=expected)
        result = buf.read_value(t)
        self.assertEqual(result, expected)
        buf.read_data.assert_called_once()

    def test_read_value_str(self):
        t = Buf.TYPE_STR
        expected = 'string'
        buf = Buf()
        buf.read_str = mock.MagicMock(return_value=expected)
        result = buf.read_value(t)
        self.assertEqual(result, expected)
        buf.read_str.assert_called_once()

    def test_read_value_unicode(self):
        t = Buf.TYPE_UNISTR
        expected = u'unicode©'
        buf = Buf()
        buf.read_str_unicode = mock.MagicMock(return_value=expected)
        result = buf.read_value(t)
        self.assertEqual(result, expected)
        buf.read_str_unicode.assert_called_once()

    def test_read_value_int64(self):
        t = Buf.TYPE_UINT64
        expected = 987654321L
        buf = Buf()
        buf.read_int64 = mock.MagicMock(return_value=expected)
        result = buf.read_value(t)
        self.assertEqual(result, expected)
        buf.read_int64.assert_called_once()

    def test_write_element(self):
        buf = Buf()
        tup = 'SomeName', 'SomeValue'
        buf.write_name = mock.MagicMock()
        buf.write_int = mock.MagicMock()
        buf.write_value = mock.MagicMock()
        buf.write_element(tup)
        buf.write_name.assert_called_once_with(tup[0])
        buf.write_int.assert_has_calls(calls=[mock.call(buf.get_type(tup[1])), mock.call(1)], any_order=True)
        buf.write_value.assert_called_once_with(tup[1])

    def test_read_element(self):
        value_type = 123
        count = 1
        name = 'name'
        value = 'value'
        buf = Buf()
        buf.read_name = mock.MagicMock(return_value=name)
        buf.read_int = mock.MagicMock()
        buf.read_int.side_effect = [value_type, count]
        buf.read_value = mock.MagicMock(return_value=value)
        result = buf.read_element()
        buf.read_name.assert_called_once()
        self.assertEqual(buf.read_int.call_count, 2)
        buf.read_value.assert_called_once_with(value_type)
        self.assertEqual(result, (name, [value]))

    def test_read_element_multiple(self):
        value_type = 456
        count = 3
        name = 'name'
        value = ['first', 'second', 'third']
        buf = Buf()
        buf.read_name = mock.MagicMock(return_value=name)
        buf.read_int = mock.MagicMock()
        buf.read_int.side_effect = [value_type, count]
        buf.read_value = mock.MagicMock()
        buf.read_value.side_effect = value
        result = buf.read_element()
        buf.read_name.assert_called_once()
        self.assertEqual(buf.read_int.call_count, 2)
        buf.read_value.assert_called_with(value_type)
        self.assertEqual(buf.read_value.call_count, count)
        self.assertEqual(result, (name, value))


if __name__ == '__main__':
    unittest.main()
