"""封存册（FENGCUNCE）· 快照谱系链式留痕，基准被改即现形。

道统映射：「册」＝册封留痕，代代相续。封存册把每一道圭影
按序入册，册册相扣（前册哈希入后册）；任何一册被改、被删、
被抽，重验时链断处即现形——基准的谱系不容事后涂改。
"""

import hashlib
import json


class Fengcunce:
    """封存册官：圭影谱系的链式账本。"""

    def __init__(self):
        self.records = []

    def append(self, shadow, note=""):
        """一道圭影入册：记序号、根哈希、条目与前册哈希。"""
        prev = self.records[-1]["hash"] if self.records else "GENESIS"
        record = {
            "seq": len(self.records) + 1,
            "root": shadow["root"],
            "entries": dict(shadow["entries"]),
            "prev": prev,
            "note": note,
        }
        record["hash"] = self._hash_record(record)
        self.records.append(record)
        return record

    @staticmethod
    def _hash_record(record):
        payload = json.dumps(
            {k: record[k] for k in ("seq", "root", "entries", "prev", "note")},
            sort_keys=True, ensure_ascii=False,
            separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def verify(self):
        """重验全册：逐册重算哈希、核对前链、复算圭影根。

        全数吻合返回 (True, "")；现形即返回 (False, 断处说明)。
        """
        prev = "GENESIS"
        for record in self.records:
            if record["prev"] != prev:
                return False, "第 %d 册前链不接：记 prev=%s，应为 %s" % (
                    record["seq"], record["prev"], prev)
            if self._hash_record(record) != record["hash"]:
                return False, "第 %d 册册身被改：哈希不合" % record["seq"]
            joined = "\n".join("%s:%s" % (k, record["entries"][k])
                               for k in sorted(record["entries"]))
            root = hashlib.sha256(joined.encode("utf-8")).hexdigest()
            if root != record["root"]:
                return False, "第 %d 册条目被改：圭影根不合" % record["seq"]
            prev = record["hash"]
        return True, ""

    def lineage(self):
        """谱系一览：各册序号、根哈希与备注。"""
        return [{"seq": r["seq"], "root": r["root"], "note": r["note"]}
                for r in self.records]
