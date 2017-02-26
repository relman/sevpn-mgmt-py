# -*- coding: utf-8 -*-
from SevpnMgmtPy.admin_api.rpc_enum_farm_item import RpcEnumFarmItem


class RpcEnumFarm:
    def __init__(self, num_farm=0, farms=list()):
        self.num_farm = num_farm
        self.farms = farms

    def in_rpc_enum_farm(self, pack):
        self.num_farm = pack.get_index_count("Id")
        for i in range(0, self.num_farm):
            item = RpcEnumFarmItem(id_=pack.get_value("Id", index=i),
                                   controller=pack.get_value("Controller", index=i),
                                   connected_time=pack.get_value("ConnectedTime", index=i),
                                   ip=pack.get_value("Ip", index=i),
                                   hostname=pack.get_value("Hostname", index=i),
                                   point=pack.get_value("Point", index=i),
                                   num_sessions=pack.get_value("NumSessions", index=i),
                                   num_tcp_connections=pack.get_value("NumTcpConnections", index=i),
                                   num_hubs=pack.get_value("NumHubs", index=i),
                                   assigned_client_license=pack.get_value("AssignedClientLicense", index=i),
                                   assigned_bridge_license=pack.get_value("AssignedBridgeLicense", index=i))
            self.farms.append(item)
