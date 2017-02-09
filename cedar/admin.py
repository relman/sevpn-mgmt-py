# -*- coding: utf-8 -*-
import hashlib

from cedar import Session
from mayaqua import Buf, Pack


class Admin:
    def admin_connect(self, hub_name, password, host, port):
        session = Session(host, port)
        session.start_rpc_session()
        p = Pack()
        p.add_client_version('Softether VPN Server Manager (py)', '0.1', '0.0')
        p.add_value("method", "admin")
        p.add_value("accept_empty_password", True)
        hashed_pass = self.hash_pass(password)
        secure_pass = self.secure_password(hashed_pass, session.rpc_random)
        p.add_value("secure_password", secure_pass)
        if hub_name:
            p.add_value("hubname", hub_name)
        session.http_client_send(p, session.sock)
        answer = session.client_download_hello(session.sock)
        assert answer
        if answer.get_value('error', None):
            return None
        session.sock.settimeout(0x0fffffff)
        return session

    def rpc_call(self, session, func_name, pack=None):
        if not session:
            return
        if not pack:
            pack = Pack()
        pack.add_value("function_name", func_name)
        session.send_raw(pack)
        data = session.recv_raw()
        result = Pack()
        buf = Buf()
        buf.storage = bytearray(data)
        result.read_pack(buf)
        if result.get_value('error', None):
            print result.get_value('error')
            return None
        return result

    def secure_password(self, hashed_pass, rand):
        src = hashed_pass + rand
        return self.hash_pass(src)

    def hash_pass(self, password):
        sha = hashlib.new('SHA')
        sha.update(password)
        return bytearray(sha.digest())
