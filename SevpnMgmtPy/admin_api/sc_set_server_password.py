# -*- coding: utf-8 -*-
from SevpnMgmtPy.admin_api.rpc_set_password import RpcSetPassword
from SevpnMgmtPy.mayaqua import Pack


def sc_set_server_password(admin, password):
    hashed = admin.hash_pass(password)
    rpc = RpcSetPassword(hashed)
    pack = Pack()
    rpc.out_rpc_set_password(pack)
    ret = admin.rpc_call("SetServerPassword", pack)
    assert ret
