# -*- coding: utf-8 -*-
import mock
import unittest

from SevpnMgmtPy.cedar import Admin


class TestAdmin(unittest.TestCase):
    def test_admin_connect(self):
        hub_name = 'hub'
        password = 'password'
        host = 'host.com'
        port = 8080
        answer = mock.MagicMock()
        admin = Admin()
        with mock.patch('SevpnMgmtPy.cedar.admin.Session') as mock_sess:
            answer.get_value = mock.MagicMock(return_value=None)
            mock_sess.return_value.http_recv_pack = mock.MagicMock(return_value=answer)
            admin.send_client_info = mock.MagicMock()
            admin.admin_connect(hub_name, password, host, port)
            mock_sess.assert_called_once_with(host, port)
            mock_sess.return_value.start_rpc_session.assert_called_once()
            admin.send_client_info.assert_called_once_with(hub_name, password)
            mock_sess.return_value.http_recv_pack.assert_called_once()
            answer.get_value.assert_called_once_with('error', None)
            mock_sess.return_value.set_sock_timeout.assert_called_once()

    def test_admin_connect_answer_is_none(self):
        hub_name = 'hub'
        password = 'password'
        host = 'host.com'
        port = 8080
        admin = Admin()
        with mock.patch('SevpnMgmtPy.cedar.admin.Session') as mock_sess, self.assertRaises(AssertionError):
            admin.send_client_info = mock.MagicMock()
            mock_sess.return_value.http_recv_pack = mock.MagicMock(return_value=None)
            admin.admin_connect(hub_name, password, host, port)
            mock_sess.assert_called_once_with(host, port)
            mock_sess.return_value.start_rpc_session.assert_called_once()
            admin.send_client_info.assert_called_once_with(hub_name, password)
            mock_sess.return_value.http_recv_pack.assert_called_once()

    def test_admin_connect_answer_has_error(self):
        hub_name = 'hub'
        password = 'password'
        host = 'host.com'
        port = 8080
        answer = mock.MagicMock()
        admin = Admin()
        with mock.patch('SevpnMgmtPy.cedar.admin.Session') as mock_sess, self.assertRaises(AssertionError):
            answer.get_value = mock.MagicMock(return_value=True)
            mock_sess.return_value.http_recv_pack = mock.MagicMock(return_value=answer)
            admin.send_client_info = mock.MagicMock()
            admin.admin_connect(hub_name, password, host, port)
            mock_sess.assert_called_once_with(host, port)
            mock_sess.return_value.start_rpc_session.assert_called_once()
            admin.send_client_info.assert_called_once_with(hub_name, password)
            mock_sess.return_value.http_recv_pack.assert_called_once()
            answer.get_value.assert_called_once_with('error', None)

    def test_send_client_info(self):
        hub_name = 'hub'
        password = 'password'
        admin = Admin()
        with mock.patch('SevpnMgmtPy.cedar.admin.Pack') as mock_pack:
            admin.session = mock.MagicMock()
            admin.hash_pass = mock.MagicMock()
            admin.secure_password = mock.MagicMock()
            admin.send_client_info(hub_name, password)
            mock_pack.assert_called_once()
            mock_pack.return_value.add_client_version.assert_called_once()
            self.assertEqual(mock_pack.return_value.add_value.call_count, 4)
            admin.hash_pass.assert_called_once_with(password)
            admin.secure_password.assert_called_once_with(admin.hash_pass.return_value,
                                                          admin.session.rpc_random)
            return admin.session.http_send_pack.assert_called_once_with(mock_pack.return_value)

    def test_rpc_call_no_session(self):
        admin = Admin()
        result = admin.rpc_call('func')
        self.assertIsNone(result)

    def test_rpc_call_no_pack(self):
        func_name = 'function'
        admin = Admin()
        with mock.patch('SevpnMgmtPy.cedar.admin.Pack') as mock_pack, \
                mock.patch('SevpnMgmtPy.cedar.admin.Buf') as mock_buf:
            admin.session = mock.MagicMock()
            mock_pack.return_value.read_pack = mock.MagicMock()
            mock_pack.return_value.get_value = mock.MagicMock(return_value=None)
            result = admin.rpc_call(func_name)
            mock_pack.assert_called_once()
            mock_pack.return_value.add_value.assert_called_once_with('function_name', func_name)
            admin.session.send_raw.assert_called_once_with(mock_pack.return_value)
            admin.session.recv_raw.assert_called_once()
            mock_buf.assert_called_once_with(admin.session.recv_raw.return_value)
            mock_pack.return_value.read_pack.assert_called_once_with(mock_buf.return_value)
            mock_pack.return_value.get_value.assert_called_once_with('error', None)
            self.assertEqual(result, mock_pack.return_value)

    def test_rpc_call_answer_has_error(self):
        func_name = 'function'
        admin = Admin()
        with mock.patch('SevpnMgmtPy.cedar.admin.Pack') as mock_pack, \
                mock.patch('SevpnMgmtPy.cedar.admin.Buf') as mock_buf, \
                self.assertRaises(AssertionError):
            admin.session = mock.MagicMock()
            mock_pack.return_value.read_pack = mock.MagicMock()
            mock_pack.return_value.get_value = mock.MagicMock(return_value=True)
            result = admin.rpc_call(func_name)
            mock_pack.assert_called_once()
            mock_pack.return_value.add_value.assert_called_once_with('function_name', func_name)
            admin.session.send_raw.assert_called_once_with(mock_pack.return_value)
            admin.session.recv_raw.assert_called_once()
            mock_buf.assert_called_once_with(admin.session.recv_raw.return_value)
            mock_pack.return_value.read_pack.assert_called_once_with(mock_buf.return_value)
            self.assertIsNone(result)

    def test_secure_password(self):
        hashed = '\x01\x02\x03\x04'
        rand = '\x05\x06\x07\x08'
        expected = bytearray('\xaa\xbb\xcc\xdd')
        admin = Admin()
        admin.hash_pass = mock.MagicMock(return_value=expected)
        result = admin.secure_password(hashed, rand)
        admin.hash_pass.assert_called_once_with(hashed + rand)
        self.assertEqual(result, expected)

    def test_hash_pass(self):
        password = 'password'
        admin = Admin()
        with mock.patch('hashlib.new') as mock_hashlib:
            digest = '\x10\x1a\x1b\x1c'
            mock_hashlib.return_value.update = mock.MagicMock()
            mock_hashlib.return_value.digest = mock.MagicMock(return_value=digest)
            result = admin.hash_pass(password)
            mock_hashlib.assert_called_once_with('SHA')
            mock_hashlib.return_value.update.assert_called_with(password)
            mock_hashlib.return_value.digest.assert_called_with()
            self.assertEqual(result, bytearray(digest))

    def test_hash_pass_123456(self):
        password = '123456'
        expected = bytearray(b'\xe9:\x90\x9cJ\x17\xd2z\xb1y\xc1\xbd2:JQ$\x1e9\x03')
        admin = Admin()
        result = admin.hash_pass(password)
        self.assertEqual(result, expected)
