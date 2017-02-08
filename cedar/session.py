# -*- coding: utf-8 -*-
import socket
import ssl

from cedar import Watermark
from mayaqua import Buf, Pack


class Session:
    CONNECTING_TIMEOUT = 15.0
    HTTP_VPN_TARGET = "/vpnsvc/vpn.cgi"
    HTTP_VPN_TARGET2 = "/vpnsvc/connect.cgi"
    HTTP_CONTENT_TYPE2 = "application/octet-stream"
    HTTP_CONTENT_TYPE3 = "image/jpeg"
    HTTP_CONNECTION = "Keep-Alive"
    HTTP_KEEP_ALIVE = "timeout=15; max=19"

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None
        self.rpc_random = None

    def start_rpc_session(self):
        sock = self.client_connect_to_server()
        self.client_upload_signature(sock)
        hello = self.client_download_hello(sock)
        assert hello
        if hello.has_name('random'):
            self.rpc_random = hello.get_value('random', bytearray())
        self.sock = sock

    def client_connect_to_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.CONNECTING_TIMEOUT)
        ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1)
        ssl_sock.connect((self.host, self.port))
        return ssl_sock

    def get_host_http_header(self):
        return "{0}:{1}".format(self.host, self.port)

    def client_upload_signature(self, sock):
        header_text = \
            "POST {0} HTTP/1.1\r\n" \
            "Host: {1}\r\n" \
            "Content-Type: {2}\r\n" \
            "Connection: {3}\r\n" \
            "Content-Length: {4}\r\n" \
            "\r\n".format(
                self.HTTP_VPN_TARGET2,
                self.get_host_http_header(),
                self.HTTP_CONTENT_TYPE3,
                self.HTTP_CONNECTION,
                len(Watermark.watermark)
            )
        body = bytearray(Watermark.watermark)
        data = bytearray(header_text) + body
        sock.sendall(data)

    def client_download_hello(self, sock):
        data = sock.recv(16 * 1024)
        spl = data.split('\r\n\r\n')
        if len(spl) != 2:
            raise Exception('Bad HttpResponse')
        pack = Pack.read_pack(bytearray(spl[1]))
        return pack

    def http_date(self):
        from wsgiref.handlers import format_date_time
        from datetime import datetime
        from time import mktime

        now = datetime.now()
        stamp = mktime(now.timetuple())
        return format_date_time(stamp)

    def http_client_send(self, pack, sock):
        if not pack:
            return
        pack.create_dummy_value()
        body = pack.to_buf()
        header_text = \
            "POST {0} HTTP/1.1\r\n" \
            "Date: {1}\r\n" \
            "Host: {2}\r\n" \
            "Keep-Alive: {3}\r\n" \
            "Connection: {4}\r\n" \
            "Content-Type: {5}\r\n" \
            "Content-Length: {6}\r\n" \
            "\r\n".format(
                self.HTTP_VPN_TARGET,
                self.http_date(),
                self.get_host_http_header(),
                self.HTTP_KEEP_ALIVE,
                self.HTTP_CONNECTION,
                self.HTTP_CONTENT_TYPE2,
                len(body.storage)
            )
        data = bytearray(header_text) + body.storage
        sock.sendall(data)

    def send_raw(self, pack):
        if not self.sock:
            return
        buf = pack.to_buf()
        size_seq = Buf.int_to_bytes(len(buf.storage))
        self.sock.send(size_seq)
        self.sock.send(buf.storage)

    def recv_raw(self):
        if not self.sock:
            return
        seq = self.sock.recv(4)
        size = Buf.bytes_to_int(seq)
        data = self.sock.recv(size)
        return data
