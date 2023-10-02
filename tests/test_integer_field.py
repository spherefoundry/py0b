import unittest

from py0b import Stream, Structure
from py0b.fields import IntegerField


class IntegerFieldTestCase(unittest.TestCase):
    def test_endianness(self):
        class TestStructure(Structure):
            little1 = IntegerField.little(1)
            little2 = IntegerField.little(2)
            little4 = IntegerField.little(4)
            little8 = IntegerField.little(8)

            big1 = IntegerField.big(1)
            big2 = IntegerField.big(2)
            big4 = IntegerField.big(4)
            big8 = IntegerField.big(8)

        with Stream.with_bytes(
                bytearray.fromhex('0102030405060708090a0b0c0d0e0f0102030405060708090a0b0c0d0e0f')
        ) as stream:
            structure = TestStructure()
            data = structure.load(stream)

        self.assertEqual(data.little1, 1)
        self.assertEqual(data.little2, 0x0302)
        self.assertEqual(data.little4, 0x07060504)
        self.assertEqual(data.little8, 0x0f0e0d0c0b0a0908)

        self.assertEqual(data.big1, 1)
        self.assertEqual(data.big2, 0x0203)
        self.assertEqual(data.big4, 0x04050607)
        self.assertEqual(data.big8, 0x08090a0b0c0d0e0f)


if __name__ == '__main__':
    unittest.main()
