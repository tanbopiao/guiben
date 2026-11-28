"""封圭（FENGGUI）· 对真值集做内容寻址快照，哈希封存。

道统映射：「圭」＝测日影之圭表，量天定基准。封圭即铸圭——
对一份真值集逐项做内容寻址（SHA-256），再合成圭影根哈希。
圭影一经封出，即为量他物的基准；基准自身被改动，影随根变，现形有据。

只依赖标准库；输入规范化：bytes 原样、str 按 UTF-8、dict/list 走
键排序紧凑 JSON，保证同一内容永远得到同一哈希。
"""

import hashlib
import json


def content_digest(content):
    """任意内容的规范哈希：bytes/str/dict/list/标量一视同仁。"""
    if isinstance(content, bytes):
        data = content
    elif isinstance(content, str):
        data = content.encode("utf-8")
    else:
        data = json.dumps(content, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


class Fenggui:
    """封圭官：把真值集铸成圭影（内容寻址快照）。"""

    def seal(self, truth_set):
        """封出圭影：逐项哈希＋默克尔根。truth_set 为 {名称: 内容}。"""
        if not isinstance(truth_set, dict) or not truth_set:
            raise ValueError("封圭需非空 {名称: 内容} 真值集")
        entries = {}
        for name in sorted(truth_set):
            entries[name] = content_digest(truth_set[name])
        root = self._root_of(entries)
        return {"entries": entries, "root": root}

    @staticmethod
    def _root_of(entries):
        """圭影根：按名称序串接 name:hash 后取哈希。"""
        joined = "\n".join("%s:%s" % (k, entries[k]) for k in sorted(entries))
        return hashlib.sha256(joined.encode("utf-8")).hexdigest()

    def recompute_root(self, entries):
        """对外提供根复算，供封存册与校影官交叉验证。"""
        return self._root_of(entries)
