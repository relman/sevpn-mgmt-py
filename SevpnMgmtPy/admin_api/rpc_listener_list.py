# -*- coding: utf-8 -*-


class RpcListenerList:
    def __init__(self, num_ports=0, ports=list(), enables=list(), errors=list()):
        self.num_ports = num_ports
        self.ports = ports
        self.enables = enables
        self.errors = errors

    def in_rpc_listener_list(self, pack):
        self.num_ports = pack.get_index_count("Ports")
        for i in range(0, self.num_ports):
            self.ports.append(pack.get_value("Ports", index=i))
            self.enables.append(pack.get_value("Enables", index=i))
            self.errors.append(pack.get_value("Errors", index=i))
