# -*- coding: utf-8 -*-
import unittest

from mayaqua import Buf


class TestBuf(unittest.TestCase):
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

    def test_read_bytes(self):
        value = bytearray('1234 example')
        expected = bytearray('1234 ')
        expected_offset = len(expected)
        size = 5
        buf = Buf()
        buf.storage = value
        result = buf.read_bytes(size)
        self.assertEqual(result, expected)
        self.assertEqual(buf.offset, expected_offset)

    def test_read_int(self):
        value = bytearray('\x00\x00\x00\x0ctest 123456') if Buf.is_little() \
            else bytearray('\x0c\x00\x00\x00test 123456')
        expected = 0x0c
        expected_offset = 4
        buf = Buf()
        buf.storage = value
        result = buf.read_int()
        self.assertEqual(result, expected)
        self.assertEqual(buf.offset, expected_offset)

    def test_read_data(self):
        value = bytearray('\x00\x00\x00\x08new test12345678') if Buf.is_little() \
            else bytearray('\x08\x00\x00\x00new test12345678')
        expected = 'new test'
        expected_offset = 12
        buf = Buf()
        buf.storage = value
        result = buf.read_data()
        self.assertEqual(result, expected)
        self.assertEqual(buf.offset, expected_offset)

    def test_read_name(self):
        value = bytearray('\x00\x00\x00\x0bnew string\x00321654\x00test data 123456789') if Buf.is_little() \
            else bytearray('\x0b\x00\x00\x00new string\x00321654\x00test data 123456789')
        expected = 'new string'
        expected_offset = 14
        buf = Buf()
        buf.storage = value
        result = buf.read_name()
        self.assertEqual(result, expected)
        self.assertEqual(buf.offset, expected_offset)

    def test_read_str(self):
        value = bytearray('\x00\x00\x00\x0anew string\x00321654\x00test data 123456789') if Buf.is_little() \
            else bytearray('\x0a\x00\x00\x00new string\x00321654\x00test data 123456789')
        expected = 'new string'
        expected_offset = 14
        buf = Buf()
        buf.storage = value
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
        buf = Buf()
        buf.storage = value
        result = buf.read_str_unicode()
        self.assertEqual(result, expected)
        self.assertEqual(buf.offset, expected_offset)

    def test_read_int64(self):
        value = '\x00\xab\x88\xcd\x99\xef\x11\xaa' if Buf.is_little() else '\xaa\x11\xef\x99\xcd\x88\xab\x00'
        expected = 0xab88cd99ef11aa
        buf = Buf()
        buf.storage = value
        result = buf.read_int64()
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
