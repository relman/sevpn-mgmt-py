# -*- coding: utf-8 -*-
import mock
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
