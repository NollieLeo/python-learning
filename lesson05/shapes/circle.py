"""圆。用标准库 math 的 pi。"""

from math import pi


def area(r: float) -> float:
    return pi * (r**2)


def perimeter(r: float) -> float:
    return 2 * pi * r
