# -*- coding: utf-8 -*-
from SevpnMgmtPy.admin_api.rpc_enum_farm import RpcEnumFarm


def sc_enum_farm_member(admin):
    ret = admin.rpc_call("EnumFarmMember")
    rpc = RpcEnumFarm()
    rpc.in_rpc_enum_farm(ret)
    return rpc
