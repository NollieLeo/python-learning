"""Lesson 05 课堂示例：模块、包、import 机制。

运行方式（注意是 -m，不是文件路径，原因见讲义）：
    uv run python -m lesson05.demo
"""

# ====================================================
# 一、import 的四种写法（ruff 的 I 规则要求：先 import xxx，再 from xxx import，各自按字母排）
# ====================================================
import math  # 1. 整个模块，用 math.pi 访问。相当于 import * as math from "math"
import os.path as osp  # 2. 起别名。相当于 import * as osp from "os/path"
import sys
from json import dumps as to_json  # 4. 拿一个名字并改名。相当于 import { dumps as toJson }
from pathlib import Path  # 3. 只拿一个名字。相当于 import { Path } from "pathlib"

print(math.pi, osp.sep, Path("a"), to_json({"k": 1}))

# from x import * 把 x 里所有公开名字倒进当前作用域，污染命名空间，实际项目禁止（ruff F403 会报）

# ====================================================
# 二、模块就是一个 .py 文件；import 时文件被「执行」一次，结果缓存在 sys.modules
# ====================================================
print("\n--- 第一次 import demo_pkg ---")
from lesson05 import demo_pkg  # noqa: E402  会看到 __init__.py 里的 print

print("--- 第二次 import demo_pkg ---")
import lesson05.demo_pkg  # noqa: E402, F401  什么都不打印：已经在 sys.modules 里了

print("lesson05.demo_pkg" in sys.modules)  # True
print(demo_pkg.hello("kaimin"))  # 通过包的公开 API 调用
print(demo_pkg.__all__)

# 和 Node 的对比：require 也有缓存（require.cache），ESM 也只执行一次，行为一致。
# 区别：Python 没有「默认导出」，一个模块就是一个命名空间，所有顶层名字都可以被 import。

# ====================================================
# 三、__name__：直接运行是 "__main__"，被 import 时是模块的完整名字
# ====================================================
print("\n当前文件的 __name__ =", __name__)  # 用 -m 跑是 "__main__"
print("demo_pkg.greet 的 __name__ =", demo_pkg.greet.__name__)  # lesson05.demo_pkg.greet

# ====================================================
# 四、Python 去哪找模块：sys.path，按顺序找，第一个命中的赢
# ====================================================
print("\nsys.path 前 3 项：")
for p in sys.path[:3]:
    print("  ", p or "(空字符串 = 当前目录)")
# sys.path[0] 的规则：
#   python a/b.py      -> a/              （脚本所在目录）
#   python -m a.b      -> 当前工作目录      （所以包里的文件要用 -m 跑）
#   pytest             -> 最外层 conftest.py 所在目录
# 后面跟着标准库目录、.venv/lib/.../site-packages（第三方包，相当于 node_modules）

# 这就是为什么上节课 uv run python lesson04/test_homework.py 找不到 lesson04：
# sys.path[0] 是 lesson04/ 自己，里面没有名叫 lesson04 的包。

# ====================================================
# 五、包 = 带 __init__.py 的目录；相对导入只能在包内部用
# ====================================================
# lesson05/
#   __init__.py          <- 让 lesson05 成为包
#   demo.py              <- 本文件
#   demo_pkg/
#     __init__.py        <- 包入口，定义公开 API
#     greet.py           <- from ._text import shout   (. = 同一个包)
#     _text.py           <- 下划线 = 内部模块
#
# 相对导入：from . import x / from .mod import y / from ..parent import z
# 只在「作为包的一部分被 import」时有效，直接 python greet.py 会报
# "attempted relative import with no known parent package"
# 规则：库代码用相对导入，脚本和测试用绝对导入（from lesson05.demo_pkg import hello）

# ====================================================
# 六、循环导入：a import b，b 又 import a
# ====================================================
# 现象：ImportError: cannot import name 'x' from partially initialized module
# 原因：a 执行到一半去 import b，b 又要 a 里还没定义的名字
# 解法：1) 把共用的东西抽到第三个模块  2) 在函数内部 import（延迟到调用时）
#       3) 只 import 模块不 from 它 import 名字（import a 然后 a.x）
# 和 ESM 的循环依赖问题同源，TS 里也常靠抽公共模块解决

# ====================================================
# 七、第三方包与 pyproject.toml：uv 对照 pnpm
# ====================================================
# uv add httpx            ≈ pnpm add httpx        （写入 [project].dependencies）
# uv add --dev pytest     ≈ pnpm add -D pytest    （写入 [dependency-groups].dev）
# uv remove httpx         ≈ pnpm remove httpx
# uv sync                 ≈ pnpm install          （按 uv.lock 装到 .venv）
# uv lock --upgrade       ≈ pnpm update
# uv run xxx              ≈ pnpm exec xxx         （在 .venv 里执行）
# uvx ruff                ≈ pnpx / npx ruff       （临时跑一个工具，不装进项目）
# uv.lock                 ≈ pnpm-lock.yaml        （要提交）
# .venv/                  ≈ node_modules/          （不提交）
#
# import 顺序约定（ruff 的 I 规则会自动排）：标准库 → 第三方 → 本项目，三组之间空一行
