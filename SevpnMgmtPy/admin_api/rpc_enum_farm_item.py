# -*- coding: utf-8 -*-


class RpcEnumFarmItem:
    def __init__(self, id_=0, controller=False, connected_time=0L, ip=0, hostname='', point=0, num_sessions=0,
                 num_tcp_connections=0, num_hubs=0, assigned_client_license=0, assigned_bridge_license=0):
        self.id_ = id_
        self.controller = controller
        self.connected_time = connected_time
        self.ip = ip
        self.hostname = hostname
        self.point = point
        self.num_sessions = num_sessions
        self.num_tcp_connections = num_tcp_connections
        self.num_hubs = num_hubs
        self.assigned_client_license = assigned_client_license
        self.assigned_bridge_license = assigned_bridge_license
