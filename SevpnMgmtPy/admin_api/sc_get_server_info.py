# -*- coding: utf-8 -*-
from SevpnMgmtPy.admin_api.rpc_server_info import RpcServerInfo


def sc_get_server_info(admin):
    ret = admin.rpc_call("GetServerInfo")
    rpc_server_info = RpcServerInfo()
    rpc_server_info.in_rpc_server_info(ret)
    return rpc_server_info
