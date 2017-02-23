# -*- coding: utf-8 -*-
class RpcListener:
    def __init__(self, port=0, enable=False):
        self.port = port
        self.enable = enable

    def out_rpc_listener(self, pack):
        pack.add_value("Port", self.port)
        pack.add_value("Enable", self.enable)

    def in_rpc_listener(self, pack):
        self.port = pack.get_value("Port")
        self.enable = pack.get_value("Enable")
