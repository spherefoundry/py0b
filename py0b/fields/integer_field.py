from enum import IntEnum
import struct as python_struct

from py0b.field import Field
from py0b.instance import Instance
from py0b.stream import Stream


class Endian(IntEnum):
    BIG_ENDIAN = 0
    LITTLE_ENDIAN = 1


class IntegerField(Field):
    """Field subclass for reading an integer. Supports integer in multiple sizes (1, 2, 4, 8) and endianness
    (big, little)
    """

    def __init__(self, size: int = 4, endian: Endian = Endian.BIG_ENDIAN):
        """
        Creates an Integer Field
        :param size: default to 4
        :param endian: default to Endian.BIG_ENDIAN
        """
        super().__init__()
        if size not in [1, 2, 4, 8]:
            raise Exception(f"Invalid size for Integer field specified: {size}")
        self._size = size
        self._endian = endian

    def load(self, target: Instance, stream: Stream):
        type_def = {
            1: "b",
            2: "h",
            4: "i",
            8: "q"
        }[self._size]

        endian = {
            Endian.BIG_ENDIAN: ">",
            Endian.LITTLE_ENDIAN: "<"
        }[self._endian]
        layout = f"{endian}{type_def}"
        data = stream.read(self._size)
        value = python_struct.unpack(layout, data)
        setattr(target, self.name, value[0])

    @classmethod
    def little(cls, size: int = 4):
        """Helper method for constructing a little endian IntField with the specified size (4 bytes by default)"""
        return cls(size, endian=Endian.LITTLE_ENDIAN)

    @classmethod
    def big(cls, size: int = 4):
        """Helper method for constructing a big endian IntField with the specified size (4 bytes by default)"""
        return cls(size, endian=Endian.BIG_ENDIAN)
