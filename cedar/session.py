# -*- coding: utf-8 -*-
import requests
import socket
import ssl

from cedar import Watermark
from mayaqua import Pack


class Session:
    CONNECTING_TIMEOUT = 15
    HTTP_VPN_TARGET2 = "/vpnsvc/connect.cgi"
    HTTP_CONTENT_TYPE3 = "image/jpeg"
    HTTP_CONNECTION = "Keep-Alive"

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    def new_rpc_session(self):
        sock = self.client_connect_to_server()
        self.client_upload_signature(sock)
        data = self.client_download_hello(sock)
        self.sock = sock
        return data

    def client_connect_to_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.CONNECTING_TIMEOUT)
        ssl_sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1)
        ssl_sock.connect((self.host, self.port))
        return ssl_sock

    def client_upload_signature(self, sock):
        header_text = \
            "POST {0} HTTP/1.1\r\n" \
            "Host: {1}\r\n" \
            "Content-Type: {2}\r\n" \
            "Connection: {3}\r\n" \
            "Content-Length: {4}\r\n" \
            "\r\n".format(
                self.HTTP_VPN_TARGET2,
                "{0}:{1}".format(self.host, self.port),
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
        with open('temp', 'w') as f:
            f.write(data)
        # TODO finish here
        pack = Pack.read_pack(bytearray(spl[1]))
        return pack
