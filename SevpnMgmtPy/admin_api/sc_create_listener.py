# -*- coding: utf-8 -*-
from SevpnMgmtPy.admin_api.rpc_listener import RpcListener
from SevpnMgmtPy.mayaqua import Pack


def sc_create_listener(admin, port, enable=True):
    rpc = RpcListener(port, enable)
    pack = Pack()
    rpc.out_rpc_listener(pack)
    ret = admin.rpc_call("CreateListener", pack)
    assert ret
