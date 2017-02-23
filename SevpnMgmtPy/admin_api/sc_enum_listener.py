# -*- coding: utf-8 -*-
from SevpnMgmtPy.admin_api.rpc_listener_list import RpcListenerList


def sc_enum_listener(admin):
    ret = admin.rpc_call("EnumListener")
    rpc = RpcListenerList()
    rpc.in_rpc_listener_list(ret)
    return rpc
