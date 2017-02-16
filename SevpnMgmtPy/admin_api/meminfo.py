# -*- coding: utf-8 -*-
class MemInfo:
    def __init__(self, total_memory=0L, used_memory=0L, free_memory=0L, total_phys=0L, used_phys=0L, free_phys=0L):
        self.total_memory = total_memory
        self.used_memory = used_memory
        self.free_memory = free_memory
        self.total_phys = total_phys
        self.used_phys = used_phys
        self.free_phys = free_phys

    def in_rpc_mem_info(self, pack):
        if pack is None:
            return
        self.total_memory = pack.get_value("TotalMemory")
        self.used_memory = pack.get_value("UsedMemory")
        self.free_memory = pack.get_value("FreeMemory")
        self.total_phys = pack.get_value("TotalPhys")
        self.used_phys = pack.get_value("UsedPhys")
        self.free_phys = pack.get_value("FreePhys")
