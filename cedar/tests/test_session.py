# -*- coding: utf-8 -*-
import mock
import socket
import ssl
import unittest

from cedar import Session


class TestSession(unittest.TestCase):
    def test_set_sock_timeout(self):
        timeout = 100
        sock = mock.MagicMock()
        sock.settimeout = mock.MagicMock()
        sess = Session('host', 'port')
        sess.set_sock_timeout(sock, timeout)
        sock.settimeout.assert_called_once_with(timeout)

    def test_get_host_http_header(self):
        host = 'https://example.com'
        port = '8080'
        sess = Session(host, port)
        result = sess.get_host_http_header()
        self.assertIsNotNone(result)
        self.assertEqual(result, host + ':' + port)

    def test_connect_to_server(self):
        sess = Session('host', 'port')
        sess.set_sock_timeout = mock.MagicMock()
        with mock.patch('socket.socket') as mock_socket, mock.patch('ssl.wrap_socket') as mock_wrap_sock:
            ssl_sock = mock.MagicMock()
            mock_wrap_sock.return_value = ssl_sock
            ssl_sock.connect = mock.MagicMock()
            sess.connect_to_server()
            mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
            sess.set_sock_timeout.assert_called_with(mock_socket.return_value, sess.CONNECTING_TIMEOUT)
            mock_wrap_sock.assert_called_once_with(mock_socket.return_value, ssl_version=ssl.PROTOCOL_TLSv1)
            ssl_sock.connect.assert_called_once_with((sess.host, sess.port))
            self.assertEqual(sess.sock, ssl_sock)
