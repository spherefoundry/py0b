import unittest

from py0b import Stream


class StreamTestCase(unittest.TestCase):
    def test_context_manager(self):
        with Stream.with_bytes(b'\x0102') as stream:
            self.assertFalse(stream.closed)
        self.assertTrue(stream.closed)

    def test_read_successful(self):
        try:
            with Stream.with_bytes(b'\x01\x02') as stream:
                data1 = stream.read(1)
                data2 = stream.read(1)
        except:
            self.fail("read() should not raise")
        self.assertEqual(b"\x01", data1)
        self.assertEqual(b"\x02", data2)

    def test_read_reach_limit(self):
        with Stream.with_bytes(b'\x01\x02') as stream, self.assertRaises(Exception):
            stream.read(3)


if __name__ == '__main__':
    unittest.main()
