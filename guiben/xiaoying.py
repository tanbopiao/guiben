"""校影（XIAOYING）· 任意对象集对照圭影，报出差异清单。

道统映射：「影」＝圭表日影，影不离圭。校影即测影——
拿一批待验对象逐项对照圭影，缺、多、变各报其状，
每一状都附双方哈希证据，不凭印象断言。
"""

from .fenggui import content_digest


class Xiaoying:
    """校影官：对照圭影逐项核验，出差异清单。"""

    def verify(self, shadow, candidates):
        """shadow 为封圭产物，candidates 为 {名称: 内容} 待验集。

        返回差异列表，每项含 kind（missing/extra/changed）、
        名称与哈希证据；无差异时返回空表。
        """
        if not isinstance(candidates, dict):
            raise ValueError("待验对象集须为 {名称: 内容}")
        diffs = []
        entries = shadow["entries"]
        for name in sorted(set(entries) | set(candidates)):
            if name not in candidates:
                diffs.append({"name": name, "kind": "missing",
                              "shadow": entries[name], "candidate": None})
            elif name not in entries:
                diffs.append({"name": name, "kind": "extra",
                              "shadow": None,
                              "candidate": content_digest(candidates[name])})
            else:
                got = content_digest(candidates[name])
                if got != entries[name]:
                    diffs.append({"name": name, "kind": "changed",
                                  "shadow": entries[name], "candidate": got})
        return diffs

    def conforms(self, shadow, candidates):
        """一行判等：无差异即合圭。"""
        return not self.verify(shadow, candidates)
