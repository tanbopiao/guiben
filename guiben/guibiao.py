"""圭表（GUIBIAO）· 门面：封圭→校影→封存册，三官合表。

道统映射：圭表是完整的测天仪器——表立竿，圭量影。
本门面把三官合成一台基准仪：封圭铸基准、校影量万物、
封存册守谱系。基准自身被动过，册上现形。
"""

from .fengcunce import Fengcunce
from .fenggui import Fenggui
from .xiaoying import Xiaoying


class Guibiao:
    """圭表仪：真值基准的封立、校验与谱系留痕。"""

    def __init__(self):
        self.fenggui = Fenggui()
        self.xiaoying = Xiaoying()
        self.fengcunce = Fengcunce()
        self.shadow = None

    def seal(self, truth_set, note=""):
        """封圭立基准：铸圭影并入册，返回圭影根哈希。"""
        self.shadow = self.fenggui.seal(truth_set)
        record = self.fengcunce.append(self.shadow, note=note)
        return record["root"]

    def verify(self, candidates):
        """校影：待验对象集对照当前圭影，出差异清单。"""
        if self.shadow is None:
            raise RuntimeError("圭表未封圭，无影可校")
        return self.xiaoying.verify(self.shadow, candidates)

    def conforms(self, candidates):
        """一行判等：待验对象集是否合圭。"""
        return not self.verify(candidates)

    def audit(self):
        """谱系自审：重验封存册，基准被改即现形。"""
        return self.fengcunce.verify()
