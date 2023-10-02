import unittest

from py0b import Instance, Stream, Structure
from py0b.fields import IntegerField, StructureField


class StructureFieldTestCase(unittest.TestCase):
    class InnerStructure(Structure):
        field = IntegerField.big(size=1)

    @staticmethod
    def load(structure: Structure, hex_string: str) -> Instance:
        with Stream.with_bytes(bytearray.fromhex(hex_string)) as stream:
            return structure.load(stream)

    def test_count_one(self):
        class TestStructure(Structure):
            data = StructureField(StructureFieldTestCase.InnerStructure(), count=1)

        struct = self.load(TestStructure(), '0102')

        self.assertEqual(struct.data.field, 1)

    def test_count_multiple(self):
        class TestStructure(Structure):
            data = StructureField(StructureFieldTestCase.InnerStructure(), count=3)

        struct = self.load(TestStructure(), '010504')

        self.assertEqual(3, len(struct.data))
        self.assertEqual(struct.data[0].field, 1)
        self.assertEqual(struct.data[1].field, 5)
        self.assertEqual(struct.data[2].field, 4)

    def test_count_reference(self):
        class TestStructure(Structure):
            some = IntegerField.big(size=2)
            data = StructureField(StructureFieldTestCase.InnerStructure(), count='some')

        struct = self.load(TestStructure(), '0002050406')

        self.assertEqual(2, len(struct.data))
        self.assertEqual(struct.data[0].field, 5)
        self.assertEqual(struct.data[1].field, 4)

    def test_greedy(self):
        class TestStructure(Structure):
            data = StructureField(StructureFieldTestCase.InnerStructure(), count='*')

        struct = self.load(TestStructure(), '01030702')

        self.assertEqual(4, len(struct.data))
        self.assertEqual(struct.data[0].field, 1)
        self.assertEqual(struct.data[1].field, 3)
        self.assertEqual(struct.data[2].field, 7)
        self.assertEqual(struct.data[3].field, 2)


if __name__ == '__main__':
    unittest.main()
