"""圭表三算子单测：封圭、校影、封存册与门面合流。"""
import unittest

from guiben import Fengcunce, Fenggui, Guibiao, Xiaoying, content_digest


class TestFenggui(unittest.TestCase):
    def test_seal_shape(self):
        shadow = Fenggui().seal({"规格A": "v1", "规格B": {"k": 2}})
        self.assertEqual(len(shadow["entries"]), 2)
        self.assertEqual(len(shadow["root"]), 64)

    def test_deterministic(self):
        feng = Fenggui()
        s1 = feng.seal({"a": "x", "b": "y"})
        s2 = feng.seal({"b": "y", "a": "x"})
        self.assertEqual(s1, s2)

    def test_content_change_moves_root(self):
        feng = Fenggui()
        s1 = feng.seal({"a": "x"})
        s2 = feng.seal({"a": "X"})
        self.assertNotEqual(s1["root"], s2["root"])

    def test_bytes_and_json_same_content_same_hash(self):
        self.assertEqual(content_digest("甲乙丙"), content_digest("甲乙丙".encode()))
        self.assertEqual(content_digest({"b": 1, "a": 2}),
                         content_digest({"a": 2, "b": 1}))

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            Fenggui().seal({})


class TestXiaoying(unittest.TestCase):
    def setUp(self):
        self.shadow = Fenggui().seal({"a": "1", "b": "2", "c": "3"})

    def test_conforms(self):
        ying = Xiaoying()
        self.assertEqual(ying.verify(self.shadow, {"a": "1", "b": "2", "c": "3"}), [])
        self.assertTrue(ying.conforms(self.shadow, {"c": "3", "a": "1", "b": "2"}))

    def test_diff_kinds_with_evidence(self):
        diffs = Xiaoying().verify(self.shadow, {"a": "9", "c": "3", "d": "4"})
        kinds = {d["name"]: d["kind"] for d in diffs}
        self.assertEqual(kinds, {"a": "changed", "b": "missing", "d": "extra"})
        for d in diffs:
            if d["kind"] == "changed":
                self.assertNotEqual(d["shadow"], d["candidate"])

    def test_rejects_non_dict(self):
        with self.assertRaises(ValueError):
            Xiaoying().verify(self.shadow, ["not-a-dict"])


class TestFengcunce(unittest.TestCase):
    def test_chain_verifies(self):
        ce = Fengcunce()
        ce.append(Fenggui().seal({"a": "1"}), note="首封")
        ce.append(Fenggui().seal({"a": "1", "b": "2"}), note="增项")
        ok, why = ce.verify()
        self.assertTrue(ok, why)
        self.assertEqual(len(ce.lineage()), 2)

    def test_record_tamper_revealed(self):
        ce = Fengcunce()
        ce.append(Fenggui().seal({"a": "1"}))
        ce.append(Fenggui().seal({"a": "2"}))
        ce.records[0]["note"] = "事后涂改"
        ok, why = ce.verify()
        self.assertFalse(ok)
        self.assertIn("第 1 册", why)

    def test_entry_tamper_revealed(self):
        """伪造者改条目并重算册哈希，圭影根复算仍兜底现形。"""
        ce = Fengcunce()
        ce.append(Fenggui().seal({"a": "1", "b": "2"}))
        ce.records[0]["entries"]["a"] = "0" * 64
        ce.records[0]["hash"] = ce._hash_record(ce.records[0])
        ok, why = ce.verify()
        self.assertFalse(ok)
        self.assertIn("圭影根不合", why)

    def test_deletion_revealed(self):
        ce = Fengcunce()
        ce.append(Fenggui().seal({"a": "1"}))
        ce.append(Fenggui().seal({"a": "1", "b": "2"}))
        del ce.records[0]
        ok, why = ce.verify()
        self.assertFalse(ok)
        self.assertIn("前链不接", why)


class TestGuibiao(unittest.TestCase):
    def test_full_flow(self):
        table = Guibiao()
        root = table.seal({"真值甲": "基线一", "真值乙": [1, 2, 3]}, note="v1 基线")
        self.assertEqual(len(root), 64)
        self.assertEqual(table.verify({"真值甲": "基线一", "真值乙": [1, 2, 3]}), [])
        self.assertTrue(table.conforms({"真值甲": "基线一", "真值乙": [1, 2, 3]}))
        diffs = table.verify({"真值甲": "被改了", "真值乙": [1, 2, 3]})
        self.assertEqual(diffs[0]["kind"], "changed")
        ok, why = table.audit()
        self.assertTrue(ok, why)

    def test_baseline_tamper_revealed(self):
        table = Guibiao()
        table.seal({"a": "1"})
        table.fengcunce.records[0]["entries"]["a"] = "f" * 64
        ok, why = table.audit()
        self.assertFalse(ok)

    def test_verify_before_seal(self):
        with self.assertRaises(RuntimeError):
            Guibiao().verify({})


if __name__ == "__main__":
    unittest.main()
