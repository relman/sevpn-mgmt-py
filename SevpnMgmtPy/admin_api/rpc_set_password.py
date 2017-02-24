# -*- coding: utf-8 -*-
class RpcSetPassword:
    def __init__(self, hashed_password):
        self.hashed_password = hashed_password

    def out_rpc_set_password(self, pack):
        pack.add_value("HashedPassword", self.hashed_password)
