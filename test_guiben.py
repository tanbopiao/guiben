"""圭本（GUIBEN）算子单测：名帖完整、行为达标、只增不覆盖。"""
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

    def test_freeze_compare(self):
        self.op.freeze({"a": 1, "b": 2})
        self.assertEqual(self.op.compare({"a": 1, "b": 2}), [])
        diffs = self.op.compare({"a": 9, "c": 3})
        kinds = {d["key"]: d["kind"] for d in diffs}
        self.assertEqual(kinds, {"a": "changed", "b": "missing", "c": "extra"})
        with self.assertRaises(RuntimeError):
            Guiben().compare({})


if __name__ == "__main__":
    unittest.main()
