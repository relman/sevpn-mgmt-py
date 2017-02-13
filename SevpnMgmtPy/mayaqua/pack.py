# -*- coding: utf-8 -*-
import collections
import platform
import random


class Pack:
    HTTP_PACK_RAND_SIZE_MAX = 1000
    ALLOWED_TYPES = [bool, int, str, bytearray, unicode, long, list]

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
        result = self._pack.get(name, default)
        if result is not None and len(result) == 1:
            return result[0]
        return result

    def add_client_version(self, client_str, client_ver, client_build):
        self.add_value('client_str', client_str)
        self.add_value('client_ver', client_ver)
        self.add_value('client_build', client_build)

    def get_platform(self):
        return platform

    def add_win_ver(self):
        p = self.get_platform()
        self.add_value('V_IsWindows', p.system() == 'Windows')
        self.add_value('V_IsNT', p.system() == 'Windows')
        self.add_value('V_IsServer', False)
        self.add_value('V_IsBeta', False)
        release = p.release()
        spl_release = release.split('.') or [0, 0]
        self.add_value('V_VerMajor', int(spl_release[0]))
        self.add_value('V_VerMinor', int(spl_release[1]))
        self.add_value('V_Build', 0)
        self.add_value('V_ServicePack', 0)
        self.add_value('V_Title', p.platform())

    def add_value(self, name, value):
        t = type(value)
        if t is bool:
            self._pack[name] = 1 if value else 0
        elif t in self.ALLOWED_TYPES:
            self._pack[name] = value
        else:
            raise Exception('Not supported value type')

    def to_buf(self, buf):
        buf.write_int(len(self._pack))
        for i in self._pack.items():
            buf.write_element(i)

    def create_dummy_value(self):
        size = random.randint(0, self.HTTP_PACK_RAND_SIZE_MAX)
        rnd = random._urandom(size)
        self.add_value('pencore', rnd)
