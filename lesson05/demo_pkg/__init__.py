"""demo_pkg 包的入口。import demo_pkg 时这个文件会被执行一次。"""

print(f"[demo_pkg/__init__.py 被执行] __name__ = {__name__}")

# 包的「公开 API」：把子模块里的东西提到包这一层，调用方就不用知道内部文件结构
from .greet import hello  # noqa: E402 —— 相对导入：. 表示当前包

__all__ = ["hello"]  # from demo_pkg import * 时只导出这些；也是给读者看的「公开清单」
