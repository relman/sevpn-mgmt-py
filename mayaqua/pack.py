# -*- coding: utf-8 -*-
import collections
import platform
import random

from mayaqua import Buf


class Pack:
    HTTP_PACK_RAND_SIZE_MAX = 1000

    def __init__(self):
        self._pack = collections.OrderedDict()

    def write_element(self, buf, tup):
        if not buf or not tup:
            return
        name, value = tup
        buf.write_str(name)
        buf.write_int(Buf.get_type(value))
        buf.write_int(1)
        buf.write_value(value)

    @classmethod
    def read_element(cls, buf):
        if not buf:
            return
        name_ = buf.read_name()
        type_ = buf.read_int()
        count = buf.read_int()
        value = buf.read_value(type_)
        return name_, value  # assuming there are always 1 value

    @classmethod
    def read_pack(cls, ba):
        if ba is None:
            return None
        p = Pack()
        buf = Buf()
        buf.storage = ba
        num = buf.read_int()
        for _ in range(0, num):
            t = cls.read_element(buf)
            p.add_value(t[0], t[1])
        return p

    def add_client_version(self, client_str, client_ver, client_build):
        self.add_value('client_str', client_str)
        self.add_value('client_ver', client_ver)
        self.add_value('client_build', client_build)

    def add_win_ver(self):
        self.add_value('V_IsWindows', platform.system() == 'Windows')
        self.add_value('V_IsNT', platform.system() == 'Windows')
        self.add_value('V_IsServer', False)
        self.add_value('V_IsBeta', False)
        release = platform.release()
        spl_release = release.split('.') or [0, 0]
        self.add_value('V_VerMajor', int(spl_release[0]))
        self.add_value('V_VerMinor', int(spl_release[1]))
        self.add_value('V_Build', 0)
        self.add_value('V_ServicePack', 0)
        self.add_value('V_Title', platform.platform())

    def add_value(self, name, value):
        if type(value) is bool:  # bool
            self._pack[name] = 1 if value else 0
        else:  # int, str, bytearray
            self._pack[name] = value

    def to_buf(self):
        buf = Buf()
        buf.write_int(len(self._pack))
        for i in self._pack.items():
            self.write_element(buf, i)
        return buf

    def create_dummy_value(self):
        size = random.randint(0, self.HTTP_PACK_RAND_SIZE_MAX)
        rnd = random._urandom(size)
        self.add_value("pencore", rnd)
