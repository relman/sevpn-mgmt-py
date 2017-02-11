# -*- coding: utf-8 -*-
import mock
import socket
import ssl
import unittest

from cedar import Session, Watermark


class TestSession(unittest.TestCase):
    def test_start_rpc_session(self):
        ba = bytearray('\xab\xcd\xef')
        hello_pack = mock.MagicMock()
        hello_pack.get_value = mock.MagicMock(return_value=ba)
        sess = Session('host', 'port')
        sess.connect_to_server = mock.MagicMock()
        sess.upload_signature = mock.MagicMock()
        sess.http_recv_pack = mock.MagicMock(return_value=hello_pack)
        sess.start_rpc_session()
        sess.connect_to_server.assert_called_once()
        sess.upload_signature.assert_called_once()
        sess.http_recv_pack.assert_called_once()
        hello_pack.get_value.assert_called_once_with('random', bytearray())
        self.assertEqual(sess.rpc_random, ba)

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

    def test_upload_signature(self):
        host, port = 'example.com', 80
        head = bytearray(
            "POST /vpnsvc/connect.cgi HTTP/1.1\r\n"
            "Host: {0}\r\n"
            "Content-Type: image/jpeg\r\n"
            "Connection: Keep-Alive\r\n"
            "Content-Length: 1411\r\n"
            "\r\n".format(
                host + ':' + str(port)
            ))
        body = bytearray(Watermark.watermark)
        sess = Session(host, port)
        sess.sock = mock.MagicMock()
        sess.sock.sendall = mock.MagicMock()
        sess.upload_signature()
        sess.sock.sendall.assert_called_once_with(head + body)

    def test_http_recv_pack_exception(self):
        sock = mock.MagicMock()
        sock.recv = mock.MagicMock(return_value=bytearray())
        sess = Session('host', 'port')
        sess.sock = sock
        with self.assertRaises(Exception):
            sess.http_recv_pack()

    def test_http_recv_pack_ok(self):
        data = bytearray('header\r\n\r\nbody')
        sock = mock.MagicMock()
        sock.recv = mock.MagicMock(return_value=data)
        sess = Session('host', 'port')
        sess.sock = sock
        with mock.patch('cedar.session.Pack') as mock_pack, mock.patch('cedar.session.Buf') as mock_buf:
            mock_pack.return_value.read_pack = mock.MagicMock()
            pack = sess.http_recv_pack()
            mock_pack.assert_called_once()
            mock_buf.assert_called_once()
            mock_pack.return_value.read_pack.assert_called_with(mock_buf.return_value)
            self.assertEqual(pack, mock_pack.return_value)

    def test_http_date(self):
        sess = Session('host', 'port')
        m1 = mock.MagicMock()
        m2 = mock.MagicMock()
        with mock.patch.dict('sys.modules', {'time': m1, 'wsgiref.handlers': m2}):
            date = sess.http_date()
            m1.mktime.assert_called_once()
            m2.format_date_time.assert_called_once_with(m1.mktime.return_value)
            self.assertEqual(date, m2.format_date_time.return_value)
