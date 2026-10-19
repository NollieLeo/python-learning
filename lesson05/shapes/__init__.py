"""作业包 shapes：包入口。

要求：
1. 用相对导入从 .circle / .rect 把 area、perimeter 提到包这一层，
   分别命名为 circle_area / circle_perimeter / rect_area / rect_perimeter。
2. 定义 describe(kind, **dims) -> str（见下方）。
3. __all__ 只列出上面 4 个函数和 describe，不要暴露 _format 里的东西。
"""

# TODO: 相对导入

__all__: list[str] = []  # TODO


def describe(kind: str, **dims: float) -> str:
    """describe("circle", r=1) -> "circle: area=3.14, perimeter=6.28"
    describe("rect", w=2, h=3) -> "rect: area=6.00, perimeter=10.00"
    kind 不认识 -> ValueError(f"unknown shape: {kind!r}")
    数字用 ._format.fmt 格式化（保留 2 位小数）。
    """
    raise NotImplementedError  # TODO
