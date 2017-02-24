# -*- coding: utf-8 -*-
class RpcFarm:
    def __init__(self, server_type=0, num_port=0, ports=list(), public_ip=0, controller_name='', controller_port=0,
                 member_password='', weight=0, controller_only=False):
        self.server_type = server_type
        self.num_port = num_port
        self.ports = ports
        self.public_ip = public_ip
        self.controller_name = controller_name
        self.controller_port = controller_port
        self.member_password = member_password
        self.weight = weight
        self.controller_only = controller_only

    def in_rpc_farm(self, pack):
        self.server_type = pack.get_value("ServerType")
        self.num_port = pack.get_index_count("Ports")
        for i in range(0, self.num_port):
            self.ports.append(pack.get_value("Ports", index=i))
        self.public_ip = pack.get_value("PublicIp")
        self.controller_name = pack.get_value("ControllerName")
        self.controller_port = pack.get_value("ControllerPort")
        self.member_password = pack.get_value("MemberPassword")
        self.weight = pack.get_value("Weight")
        self.controller_only = pack.get_value("ControllerOnly")
