import unittest

from py0b import Instance
from py0b.amount import StaticAmount, ReferenceAmount, GreedyAmount


class StaticAmountTestCase(unittest.TestCase):
    def test_direct(self):
        self.assertEqual(3, StaticAmount(3).resolve(Instance()))


class ReferenceAmountTestCase(unittest.TestCase):
    def test_correct(self):
        target = Instance()
        target.some_name = 6
        self.assertEqual(6, ReferenceAmount('some_name').resolve(target))

    def test_missing_reference(self):
        target = Instance()
        target.some_name = 6
        with self.assertRaises(Exception):
            ReferenceAmount('other_name').resolve(target)

    def test_incorrect_reference_type(self):
        target = Instance()
        target.some_name = "data"
        with self.assertRaises(Exception):
            ReferenceAmount('some_name').resolve(target)


class GreedyAmountTestCase(unittest.TestCase):
    def test_correct(self):
        with self.assertRaises(Exception):
            GreedyAmount().resolve(Instance())


if __name__ == '__main__':
    unittest.main()
