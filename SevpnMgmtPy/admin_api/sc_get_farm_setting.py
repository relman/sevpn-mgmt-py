# -*- coding: utf-8 -*-
from SevpnMgmtPy.admin_api.rpc_farm import RpcFarm


def sc_get_farm_setting(admin):
    ret = admin.rpc_call("GetFarmSetting")
    rpc = RpcFarm()
    rpc.in_rpc_farm(ret)
    return rpc
