# -*- coding: utf-8 -*-
from SevpnMgmtPy.admin_api.rpc_listener import RpcListener
from SevpnMgmtPy.mayaqua import Pack


def sc_enable_listener(admin, port, enable):
    rpc = RpcListener(port, enable)
    pack = Pack()
    rpc.out_rpc_listener(pack)
    ret = admin.rpc_call("EnableListener", pack)
    rpc.in_rpc_listener(ret)
    return rpc
