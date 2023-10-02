import unittest

from py0b import Stream, Structure, Instance
from py0b.fields import BytesField, IntegerField


class BytesFieldTestCase(unittest.TestCase):
    @staticmethod
    def load(structure: Structure, hex_string: str) -> Instance:
        with Stream.with_bytes(bytearray.fromhex(hex_string)) as stream:
            return structure.load(stream)

    def test_direct_size(self):
        class TestStructure(Structure):
            first = BytesField(size=4)
            second = BytesField(size=6)

        data = self.load(TestStructure(), '0102030405060708090a')

        self.assertEqual(data.first, bytearray.fromhex('01020304'))
        self.assertEqual(data.second, bytearray.fromhex('05060708090a'))

    def test_reference_size(self):
        class TestStructure(Structure):
            some = IntegerField.big(size=2)
            data = BytesField(size='some')

        data = self.load(TestStructure(), '000401020304')

        self.assertEqual(data.some, 4)
        self.assertEqual(data.data, bytearray.fromhex('01020304'))


if __name__ == '__main__':
    unittest.main()
