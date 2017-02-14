# -*- coding: utf-8 -*-
import mock
import random
import unittest

from SevpnMgmtPy.mayaqua import Pack


class TestPack(unittest.TestCase):
    def test_read_pack(self):
        num = 2
        mock_buf = mock.MagicMock()
        mock_buf.read_int = mock.MagicMock(return_value=num)
        mock_buf.read_element = mock.MagicMock()
        mock_buf.read_element.side_effect = [(1, 2), (3, 4)]
        p = Pack()
        p.add_value = mock.MagicMock()
        p.read_pack(mock_buf)
        mock_buf.read_int.assert_called_once()
        mock_buf.read_element.assert_called()
        p.add_value.assert_has_calls(calls=[mock.call(1, 2), mock.call(3, 4)])

    def test_get_value(self):
        name = 'test'
        value = 'value'
        p = Pack()
        p.add_value(name, value)
        result = p.get_value(name)
        self.assertEqual(result, value)

    def test_get_value_none(self):
        p = Pack()
        result = p.get_value('test')
        self.assertIsNone(result)

    def test_get_value_multiple(self):
        name = 'list'
        value = [1, 2, 3]
        p = Pack()
        p.add_value(name, value)
        result = p.get_value(name)
        self.assertEqual(result, value)

    def test_get_value_by_index(self):
        name = 'num_array'
        value = [10, 20, 30]
        index = 2
        p = Pack()
        p.add_value(name, value)
        result = p.get_value(name, index=index)
        self.assertEqual(result, value[index])

    def test_get_value_index_out_of_range(self):
        name = 'num_array'
        value = [10, 20, 30]
        index = 5
        p = Pack()
        p.add_value(name, value)
        with self.assertRaises(IndexError):
            result = p.get_value(name, index=index)
            self.assertIsNone(result)

    def test_add_client_version(self):
        client_str = 'Client Str'
        client_ver = 'Client Ver'
        client_build = 'Client Build'
        p = Pack()
        p.add_value = mock.MagicMock()
        p.add_client_version(client_str, client_ver, client_build)
        p.add_value.assert_has_calls(calls=[mock.call('client_str', client_str),
                                            mock.call('client_ver', client_ver),
                                            mock.call('client_build', client_build)],
                                     any_order=True)

    def test_get_platform(self):
        p = Pack()
        result = p.get_platform()
        self.assertIsNotNone(result)
        self.assertEqual(result.__name__, 'platform')

    def test_add_win_ver(self):
        p = Pack()
        p.add_value = mock.MagicMock()
        p.get_platform = mock.MagicMock()
        p.get_platform.system = mock.MagicMock()
        p.get_platform.platform = mock.MagicMock()
        p.get_platform.release = mock.MagicMock(return_value='')
        p.add_win_ver()
        p.add_value.assert_called()
        p.get_platform.assert_called_once()

    def test_add_value_bool(self):
        name = 'BoolVal'
        value = True
        p = Pack()
        p.add_value(name, value)
        self.assertEqual(len(p._pack), 1)
        self.assertEqual(p._pack[name], value)

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

    def test_add_value_list(self):
        name = 'ListVal'
        value = [1, 2, 3]
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

    def test_to_buf(self):
        di = {'value1': 123, 'value2': 'abc'}
        buf = mock.MagicMock()
        buf.write_int = mock.MagicMock()
        buf.write_element = mock.MagicMock()
        pack = Pack()
        pack._pack = di
        pack.to_buf(buf)
        buf.write_int.assert_called_once_with(len(di.items()))
        buf.write_element.assert_has_calls(calls=[mock.call(di.items()[0]), mock.call(di.items()[1])], any_order=True)

    def test_create_dummy_value(self):
        name = 'pencore'
        p = Pack()
        p.create_dummy_value()
        self.assertEqual(len(p._pack), 1)
        self.assertTrue(name in p._pack)
        self.assertTrue(len(p._pack[name]) < p.HTTP_PACK_RAND_SIZE_MAX)

    def test_get_index_count_none(self):
        p = Pack()
        result = p.get_index_count('test')
        self.assertEqual(result, 0)

    def test_get_index_count(self):
        name = 'test'
        value = [1, 2, 3]
        p = Pack()
        p.add_value(name, value)
        result = p.get_index_count(name)
        self.assertEqual(result, len(value))


if __name__ == '__main__':
    unittest.main()
