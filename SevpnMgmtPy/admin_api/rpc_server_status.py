# -*- coding: utf-8 -*-
from SevpnMgmtPy.admin_api.meminfo import MemInfo
from SevpnMgmtPy.admin_api.traffic import Traffic


class RpcServerStatus:
    def __init__(self, server_type=0, num_tcp_connections=0, num_tcp_connections_local=0, num_tcp_connections_remote=0,
                 num_hub_total=0, num_hub_standalone=0, num_hub_static=0, num_hub_dynamic=0, num_sessions_total=0,
                 num_sessions_local=0, num_sessions_remote=0, num_mac_tables=0, num_ip_tables=0, num_users=0,
                 num_groups=0, assigned_bridge_licenses=0, assigned_client_licenses=0, assigned_bridge_licenses_total=0,
                 assigned_client_licenses_total=0, traffic=Traffic(), current_time=0L, current_tick=0L, start_time=0L,
                 mem_info=MemInfo()):
        self.server_type = server_type
        self.num_tcp_connections = num_tcp_connections
        self.num_tcp_connections_local = num_tcp_connections_local
        self.num_tcp_connections_remote = num_tcp_connections_remote
        self.num_hub_total = num_hub_total
        self.num_hub_standalone = num_hub_standalone
        self.num_hub_static = num_hub_static
        self.num_hub_dynamic = num_hub_dynamic
        self.num_sessions_total = num_sessions_total
        self.num_sessions_local = num_sessions_local
        self.num_sessions_remote = num_sessions_remote
        self.num_mac_tables = num_mac_tables
        self.num_ip_tables = num_ip_tables
        self.num_users = num_users
        self.num_groups = num_groups
        self.assigned_bridge_licenses = assigned_bridge_licenses
        self.assigned_client_licenses = assigned_client_licenses
        self.assigned_bridge_licenses_total = assigned_bridge_licenses_total
        self.assigned_client_licenses_total = assigned_client_licenses_total
        self.traffic = traffic
        self.current_time = current_time
        self.current_tick = current_tick
        self.start_time = start_time
        self.mem_info = mem_info

    def in_rpc_server_status(self, pack):
        if pack is None:
            return
        self.server_type = pack.get_value("ServerType")
        self.num_tcp_connections = pack.get_value("NumTcpConnections")
        self.num_tcp_connections_local = pack.get_value("NumTcpConnectionsLocal")
        self.num_tcp_connections_remote = pack.get_value("NumTcpConnectionsRemote")
        self.num_hub_total = pack.get_value("NumHubTotal")
        self.num_hub_standalone = pack.get_value("NumHubStandalone")
        self.num_hub_static = pack.get_value("NumHubStatic")
        self.num_hub_dynamic = pack.get_value("NumHubDynamic")
        self.num_sessions_total = pack.get_value("NumSessionsTotal")
        self.num_sessions_local = pack.get_value("NumSessionsLocal")
        self.num_sessions_remote = pack.get_value("NumSessionsRemote")
        self.num_mac_tables = pack.get_value("NumMacTables")
        self.num_ip_tables = pack.get_value("NumIpTables")
        self.num_users = pack.get_value("NumUsers")
        self.num_groups = pack.get_value("NumGroups")
        self.current_time = pack.get_value("CurrentTime")
        self.current_tick = pack.get_value("CurrentTick")
        self.assigned_bridge_licenses = pack.get_value("AssignedBridgeLicenses")
        self.assigned_client_licenses = pack.get_value("AssignedClientLicenses")
        self.assigned_bridge_licenses_total = pack.get_value("AssignedBridgeLicensesTotal")
        self.assigned_client_licenses_total = pack.get_value("AssignedClientLicensesTotal")
        self.start_time = pack.get_value("StartTime")
        traffic = Traffic()
        traffic.in_rpc_traffic(pack)
        self.traffic = traffic
        self.mem_info = MemInfo().in_rpc_mem_info(pack)
