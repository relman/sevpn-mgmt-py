# -*- coding: utf-8 -*-
class RpcTest:
    def __init__(self, int_val=0, int64_val=0L, str_val='', unistr_val=u''):
        self.int_val = int_val
        self.int64_val = int64_val
        self.str_val = str_val
        self.unistr_val = unistr_val

    def in_rpc_test(self, pack):
        self.int_val = pack.get_value("IntValue")
        self.int64_val = pack.get_value("Int64Value")
        self.str_val = pack.get_value("StrValue")
        self.unistr_val = pack.get_value("UniStrValue")

    def out_rpc_test(self, pack):
        pack.add_value("IntValue", self.int_val)
        pack.add_value("Int64Value", self.int64_val)
        pack.add_value("StrValue", self.str_val)
        pack.add_value("UniStrValue", self.unistr_val)
