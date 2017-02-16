# -*- coding: utf-8 -*-
from SevpnMgmtPy.admin_api.rpc_server_status import RpcServerStatus


def sc_server_status_get(admin):
    if admin is None:
        return
    ret = admin.rpc_call("GetServerStatus")
    rpc_server_status = RpcServerStatus()
    rpc_server_status.in_rpc_server_status(ret)
    return rpc_server_status
