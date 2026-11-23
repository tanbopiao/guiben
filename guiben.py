"""圭本（GUIBEN）· 基线快照全局真值基准包

道统出处：元极恒一·道统构件定名册 V1.0 全量编译补录 ｜ 第五批
体系锚：Ω₀⊂⊙∞⊂Ω｜DID-BR-000002

工程映射：基线快照全局真值基准包。

边界：本件为算子骨架 v0——接口先立、实现随进化轮补齐；遵循元法第四条「只增不覆盖」，
方法只增不改名不删，行为变更走新版本；凭据不入档，宣称与事实分离。
"""

class Guiben:
    """圭本（GUIBEN）算子骨架 v0。"""

    ANCHOR = "Ω₀⊂⊙∞⊂Ω｜DID-BR-000002"
    CODE = "GUIBEN"

    def __init__(self, config=None):
        self.config = dict(config or {})
        self.events = []  # 只增不覆盖：会话内事件留痕

    def describe(self):
        """构件名帖：名、代号、职责、铭文、体系锚。"""
        return {
            "repo": "guiben",
            "cn": "圭本",
            "code": self.CODE,
            "duty": "基线快照全局真值基准包",
            "mingwen": "圭本为基，真值不二",
            "anchor": self.ANCHOR,
        }

    def freeze(self, state):
        """圭本为基：冻结基线快照，返回真值哈希（骨架桩：实现随进化轮补齐）。"""
        raise NotImplementedError("GUIBEN.freeze 骨架桩，候进化轮补齐")

    def compare(self, state):
        """与圭本比对，出圭舛清单（骨架桩：实现随进化轮补齐）。"""
        raise NotImplementedError("GUIBEN.compare 骨架桩，候进化轮补齐")
