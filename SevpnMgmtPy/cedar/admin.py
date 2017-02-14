# -*- coding: utf-8 -*-
import hashlib

from session import Session
from SevpnMgmtPy.mayaqua import Buf, Pack


class Admin:
    def __init__(self):
        self.session = None

    def admin_connect(self, hub_name, password, host, port):
        self.session = Session(host, port)
        self.session.start_rpc_session()
        self.send_client_info(hub_name, password)
        answer = self.session.http_recv_pack()
        assert answer
        assert answer.get_value('error', None) is None
        self.session.set_sock_timeout(self.session.sock, 0x0fffffff)

    def send_client_info(self, hub_name, password):
        p = Pack()
        p.add_client_version('Softether VPN Server Manager (py)', '0.1', '0.0')
        p.add_value("method", "admin")
        p.add_value("accept_empty_password", True)
        hashed_pass = self.hash_pass(password)
        secure_pass = self.secure_password(hashed_pass, self.session.rpc_random)
        p.add_value("secure_password", secure_pass)
        if hub_name:
            p.add_value("hubname", hub_name)
        self.session.http_send_pack(p)

    def rpc_call(self, func_name, pack=None):
        if not self.session or not func_name:
            return None
        if not pack:
            pack = Pack()
        pack.add_value("function_name", func_name)
        self.session.send_raw(pack)
        data = self.session.recv_raw()
        buf = Buf(data)
        pack.read_pack(buf)
        assert pack.get_value('error', None) is None
        return pack

    def secure_password(self, hashed_pass, rand):
        src = hashed_pass + rand
        return self.hash_pass(src)

    def hash_pass(self, password):
        sha = hashlib.new('SHA')
        sha.update(password)
        return bytearray(sha.digest())
