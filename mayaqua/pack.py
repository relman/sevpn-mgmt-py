# -*- coding: utf-8 -*-
import collections
import platform
import random

from mayaqua import Buf


class Pack:
    HTTP_PACK_RAND_SIZE_MAX = 1000
    ALLOWED_TYPES = [bool, int, str, bytearray, unicode, long]

    def __init__(self):
        self._pack = collections.OrderedDict()

    def read_pack(self, buf):
        if buf is None:
            return None
        num = buf.read_int()
        for _ in range(0, num):
            t = buf.read_element()
            self.add_value(t[0], t[1])

    def has_name(self, name):
        return name in self._pack

    def get_value(self, name, default=None):
        return self._pack.get(name, default)

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
        t = type(value)
        if t is bool:
            self._pack[name] = 1 if value else 0
        elif t in self.ALLOWED_TYPES:
            self._pack[name] = value
        else:
            raise Exception('Not supported value type')

    def to_buf(self):
        buf = Buf()
        buf.write_int(len(self._pack))
        for i in self._pack.items():
            buf.write_element(i)
        return buf

    def create_dummy_value(self):
        size = random.randint(0, self.HTTP_PACK_RAND_SIZE_MAX)
        rnd = random._urandom(size)
        self.add_value('pencore', rnd)
