# -*- coding: utf-8 -*-
from SevpnMgmtPy.admin_api.rpc_test import RpcTest
from SevpnMgmtPy.mayaqua import Pack


def sc_crash(admin):
    if admin is None:
        return
    pack = Pack()
    rpc_test = RpcTest()
    rpc_test.out_rpc_test(pack)
    ret = admin.rpc_call("Crash", pack=pack)
    return rpc_test.in_rpc_test(ret)
