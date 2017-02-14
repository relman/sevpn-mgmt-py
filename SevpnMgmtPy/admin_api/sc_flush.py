# -*- coding: utf-8 -*-
from SevpnMgmtPy.admin_api.rpc_test import RpcTest
from SevpnMgmtPy.mayaqua import Pack


def sc_flush(admin):
    pack = Pack()
    rpc_test = RpcTest()
    rpc_test.out_rpc_test(pack)
    ret = admin.rpc_call("Flush", pack=pack)
    return rpc_test.in_rpc_test(ret)
