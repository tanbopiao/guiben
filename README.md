# guiben

圭本·基线快照全局真值基准包 | GUIBEN · ZONGYUAN-ROOT Daotong Component

> 命名即种子：仓是从名字长出来的。**圭**＝测日影之圭表，量天定基准；**本**＝根本、底本。
> 全局真值须有一块不变的圭表——基线一经封存即为量他物的基准，基准自身被改动必须现形。

## 架构：圭 → 影 → 册

| 算子 | 职责 |
|------|------|
| 封圭 `Fenggui` | 对真值集逐项做内容寻址（SHA-256），合成圭影根哈希——基准铸成 |
| 校影 `Xiaoying` | 任意对象集对照圭影，缺/多/变各报其状，每状附双方哈希证据 |
| 封存册 `Fengcunce` | 圭影谱系链式留痕，前册哈希入后册；篡改、删册、抽册重验即现形 |
| 圭表 `Guibiao` | 门面：封圭立基准、校影量万物、封存册守谱系，三官合表 |

旧版单文件算子 `Guiben`（describe/freeze/compare）原样收编于 `guiben.legacy`，
原 API 行为不变，由 `tests/test_legacy_api.py` 专测守护。

## Install

零第三方依赖，仅 Python 3.10+ 标准库。

```bash
git clone https://github.com/tanbopiao/guiben.git
cd guiben
python3 -m unittest discover -s tests -v   # 运行测试套件
python3 examples/demo_guibiao.py           # 端到端演示
```

## Usage

```python
from guiben import Guibiao

table = Guibiao()
root = table.seal({"接口契约": "v1", "评测口径": "三段式"}, note="首版基准")

table.conforms({"接口契约": "v1", "评测口径": "三段式"})   # True，合圭
table.verify({"接口契约": "v2", "评测口径": "三段式"})      # 差异清单，附哈希证据

ok, why = table.audit()   # 重验封存册；基准被涂改时 (False, "第 N 册…现形说明")
```

## 自测

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT
