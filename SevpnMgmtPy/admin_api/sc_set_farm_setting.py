# -*- coding: utf-8 -*-
from SevpnMgmtPy.admin_api.rpc_farm import RpcFarm
from SevpnMgmtPy.mayaqua import Pack


def sc_set_farm_setting(admin, rpc=RpcFarm()):
    pack = Pack()
    rpc.out_rpc_farm(pack)
    ret = admin.rpc_call("SetFarmSetting", pack)
    assert ret
