# -*- coding: utf-8 -*-
from SevpnMgmtPy.admin_api.rpc_test import RpcTest
from SevpnMgmtPy.mayaqua import Pack


def sc_debug(admin, id_, arg):
    pack = Pack()
    rpc_test = RpcTest(int_val=id_, str_val=arg)
    rpc_test.out_rpc_test(pack)
    ret = admin.rpc_call("Debug", pack=pack)
    return rpc_test.in_rpc_test(ret)
