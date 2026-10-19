"""一个普通模块。"""

from ._text import shout  # 相对导入同包的私有模块（下划线开头 = 内部实现）

DEFAULT_NAME = "world"  # 模块级变量，import 时执行一次，之后所有人共享


def hello(name: str = DEFAULT_NAME) -> str:
    return shout(f"hello, {name}")
