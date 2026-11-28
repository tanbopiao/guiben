"""圭本（GUIBEN）· 基线快照全局真值基准包。

命名即种子：圭（封圭，内容寻址铸基准）→ 影（校影，对照报差异）
→ 册（封存册，谱系链式留痕，基准被改即现形）。
门面为圭表 Guibiao；旧版单文件算子 Guiben 原样收编于
guiben.legacy，原 API 行为不变（tests/test_legacy_api.py 守护）。
"""

from .fengcunce import Fengcunce
from .fenggui import Fenggui, content_digest
from .guibiao import Guibiao
from .legacy import Guiben
from .xiaoying import Xiaoying

__all__ = [
    "Guiben", "Guibiao", "Fenggui", "Xiaoying", "Fengcunce",
    "content_digest",
]
