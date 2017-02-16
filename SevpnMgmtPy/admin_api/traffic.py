# -*- coding: utf-8 -*-


class TrafficEntry:
    def __init__(self, broadcast_count=0L, broadcast_bytes=0L, unicast_count=0L, unicast_bytes=0L):
        self.broadcast_count = broadcast_count
        self.broadcast_bytes = broadcast_bytes
        self.unicast_count = unicast_count
        self.unicast_bytes = unicast_bytes


class Traffic:
    def __init__(self, send=TrafficEntry(), recv=TrafficEntry()):
        self.send = send
        self.recv = recv

    def in_rpc_traffic(self, pack):
        if pack is None:
            return
        self.recv.broadcast_bytes = pack.get_value("Recv.BroadcastBytes")
        self.recv.broadcast_count = pack.get_value("Recv.BroadcastCount")
        self.recv.unicast_bytes = pack.get_value("Recv.UnicastBytes")
        self.recv.unicast_count = pack.get_value("Recv.UnicastCount")
        self.send.broadcast_bytes = pack.get_value("Send.BroadcastBytes")
        self.send.broadcast_count = pack.get_value("Send.BroadcastCount")
        self.send.unicast_bytes = pack.get_value("Send.UnicastBytes")
        self.send.unicast_count = pack.get_value("Send.UnicastCount")
