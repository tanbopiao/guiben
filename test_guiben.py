"""圭本（GUIBEN）算子骨架单测：名帖完整、桩位齐整、只增不覆盖。"""
import unittest

from guiben import Guiben


class TestGuiben(unittest.TestCase):
    def setUp(self):
        self.op = Guiben()

    def test_describe(self):
        d = self.op.describe()
        self.assertEqual(d["repo"], "guiben")
        self.assertEqual(d["code"], "GUIBEN")
        self.assertTrue(d["anchor"].startswith("Ω₀⊂⊙∞⊂Ω"))
        self.assertTrue(d["mingwen"])

    def test_freeze_stub(self):
        with self.assertRaises(NotImplementedError):
            self.op.freeze(None)

    def test_compare_stub(self):
        with self.assertRaises(NotImplementedError):
            self.op.compare(None)


if __name__ == "__main__":
    unittest.main()
