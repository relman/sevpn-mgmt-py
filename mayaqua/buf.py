# -*- coding: utf-8 -*-
import struct
import sys


class Buf:
    TYPE_INT = 0
    TYPE_DATA = 1
    TYPE_STR = 2
    TYPE_UNISTR = 3
    TYPE_UINT64 = 4
    TYPE_UNKNOWN = 0x0fffffff
    allowed_types = [
        TYPE_INT, TYPE_DATA, TYPE_STR, TYPE_UNISTR, TYPE_UINT64
    ]

    def __init__(self, storage=None):
        if storage and type(storage) is not bytearray:
            storage = bytearray(storage)
        self.storage = storage or bytearray()
        self.offset = 0

    def __len__(self):
        return len(self.storage)

    @staticmethod
    def is_little():
        return sys.byteorder == 'little'

    @classmethod
    def get_type(cls, value):
        t = type(value)
        if t is bool or t is int:
            return cls.TYPE_INT
        if t is bytearray:
            return cls.TYPE_DATA
        if t is str:
            return cls.TYPE_STR
        if t is unicode:
            return cls.TYPE_UNISTR
        if t is long:
            return cls.TYPE_UINT64
        return cls.TYPE_UNKNOWN

    @staticmethod
    def int_to_bytes(int_val):
        modifier = '>' if Buf.is_little() else '<'
        seq = struct.pack('{0}I'.format(modifier), int_val)
        return seq

    @staticmethod
    def bytes_to_int(seq):
        modifier = '>' if Buf.is_little() else '<'
        tup = struct.unpack('{0}I'.format(modifier), seq)
        return tup[0]

    def write_int(self, value):
        seq = self.int_to_bytes(value)
        for i in seq:
            self.storage.append(i)

    def write_data(self, value):
        if value is None:
            return
        self.write_int(len(value))
        for b in value:
            self.storage.append(b)

    def write_name(self, value):
        if value is None:
            return
        self.write_int(len(value) + 1)
        for ch in value:
            self.storage.append(ch)

    def write_str(self, value):
        if value is None:
            return
        self.write_int(len(value))
        for ch in value:
            self.storage.append(ch)

    def write_str_unicode(self, value):
        if value is None:
            return
        s = value.encode('utf8')
        self.write_str(s)

    def write_int64(self, value):
        modifier = '>' if Buf.is_little() else '<'
        seq = struct.pack('{0}Q'.format(modifier), value)
        for i in seq:
            self.storage.append(i)

    def write_value(self, value):
        if value is None:
            return
        t = Buf.get_type(value)
        if t == self.TYPE_INT:
            self.write_int(value)
        elif t == self.TYPE_DATA:
            self.write_data(value)
        elif t == self.TYPE_STR:
            self.write_str(value)
        elif t == self.TYPE_UNISTR:
            self.write_str_unicode(value)
        elif t == self.TYPE_UINT64:
            self.write_int64(value)

    def read_bytes(self, size):  # TODO: add overflow validation
        result = self.storage[self.offset:(self.offset + size)]
        self.offset += size
        return result

    def read_int(self):
        seq = self.read_bytes(4)
        return self.bytes_to_int(seq)

    def read_data(self):
        len_ = self.read_int()
        seq = self.read_bytes(len_)
        return seq

    def read_name(self):
        len_ = self.read_int()
        seq = self.read_bytes(len_ - 1)
        str_ = str(seq)
        return str_

    def read_str(self):
        len_ = self.read_int()
        seq = self.read_bytes(len_)
        str_ = str(seq)
        return str_

    def read_str_unicode(self):
        s = self.read_str()
        return s.decode('utf8')

    def read_int64(self):
        seq = self.read_bytes(8)
        modifier = '>' if Buf.is_little() else '<'
        value = struct.unpack('{0}Q'.format(modifier), seq)
        return value[0]

    def read_value(self, type_):
        if type_ not in self.allowed_types:
            return None
        if type_ == self.TYPE_INT:
            return self.read_int()
        elif type_ == self.TYPE_DATA:
            return self.read_data()
        elif type_ == self.TYPE_STR:
            return self.read_str()
        elif type_ == self.TYPE_UNISTR:
            return self.read_str_unicode()
        elif type_ == self.TYPE_UINT64:
            return self.read_int64()

    def write_element(self, tup):
        if not tup:
            return
        name, value = tup
        self.write_name(name)
        self.write_int(self.get_type(value))
        self.write_int(1)
        self.write_value(value)

    def read_element(self):
        name_ = self.read_name()
        type_ = self.read_int()
        count = self.read_int()
        value = None
        for _ in range(0, count):
            value = self.read_value(type_)
        return name_, value
