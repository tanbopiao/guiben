"""圭表端到端演示：封圭立基准 → 校影量万物 → 封存册现形篡改。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from guiben import Guibiao

TRUTH = {"接口契约": "v1", "评测口径": "三段式", "样例数": 7}

table = Guibiao()
root = table.seal(TRUTH, note="首版基准")
print("封圭：基准已立，圭影根 =", root[:16], "…")

print("校影：完全一致 →", table.conforms(dict(TRUTH)))

drifted = dict(TRUTH, 样例数=6)
print("校影：样例数被改 →", table.verify(drifted))

table.fengcunce.records[0]["entries"]["接口契约"] = "0" * 64
ok, why = table.audit()
print("审计：基准被涂改 →", ok, "｜现形：", why)
