"""Lesson 07 课堂示例：类型注解。TS 工程师最舒服的一课。

运行方式：uv run python -m lesson07.demo
类型检查：uv run pyright lesson07/demo.py   （应该 0 errors）
"""

from collections.abc import Callable, Iterable, Sequence
from typing import Any, Literal, NotRequired, Protocol, TypedDict, runtime_checkable

# ====================================================
# 一、基本注解：和 TS 一样的位置，不一样的拼写
# ====================================================
name: str = "kaimin"
age: int = 28
scores: list[int] = [90, 85]  # 3.9+ 直接用内置类型做泛型，不用 typing.List
config: dict[str, int] = {"port": 8000}
pair: tuple[str, int] = ("a", 1)  # 固定长度 tuple，≈ [string, number]
nums: tuple[int, ...] = (1, 2, 3)  # 不定长，≈ number[] 但不可变
maybe: int | None = None  # ≈ number | null；3.10+ 用 |，不用 Optional[int]
either: int | str = 1  # ≈ number | string；不用 Union[int, str]
anything: Any = object()  # ≈ any，关掉检查，尽量别用


def greet(user: str, times: int = 1) -> str:
    return f"hi {user}" * times


def log(msg: str) -> None:  # 不返回就写 None，≈ void
    print(msg)


# 运行时完全不检查（Lesson 02 说过）。检查靠 pyright：
#   uv run pyright lesson07/demo.py
# VS Code 里的 Pylance 就是 pyright，红线就是它画的。pyproject.toml 的 [tool.pyright] 配严格度。

# ====================================================
# 二、Optional 与类型收窄（narrowing）：和 TS 一模一样的思路
# ====================================================


def find_user(uid: int) -> str | None:
    return "kaimin" if uid == 1 else None


u = find_user(1)
# u.upper()            # pyright: "upper" is not a known attribute of "None"
if u is not None:  # 收窄后才能用；和 TS 的 if (u !== null) 一样
    print(u.upper())
print(u.upper() if u else "nobody")  # 真值判断也能收窄


def parse_port(text: str) -> int | None:
    try:
        return int(text)
    except ValueError:
        return None


# ====================================================
# 三、容器与可迭代：参数用宽类型，返回用窄类型
# ====================================================


def total(items: Iterable[int]) -> int:  # 接受 list / tuple / set / 生成器…
    return sum(items)


def first(items: Sequence[str]) -> str:  # 需要下标就用 Sequence（list / tuple / str）
    return items[0]


print(total([1, 2]), total({3, 4}), total(x for x in range(3)), first(("a", "b")))
# 原则：参数标最宽的「我只需要这些能力」的抽象类型，返回标最具体的类型。≈ TS 里参数用 Iterable<T>

# ====================================================
# 四、Literal：字符串字面量联合，≈ "asc" | "desc"
# ====================================================
Order = Literal["asc", "desc"]  # 类型别名（简单写法）


def sort_nums(xs: list[int], order: Order = "asc") -> list[int]:
    return sorted(xs, reverse=(order == "desc"))


print(sort_nums([3, 1, 2], "desc"))
# sort_nums([1], "down")   # pyright: "down" is not assignable to Literal['asc', 'desc']

# ====================================================
# 五、TypedDict：给 dict 写 interface
# ====================================================


class Movie(TypedDict):  # ≈ interface Movie { title: string; year: number; rating?: number }
    title: str
    year: int
    rating: NotRequired[float]  # 可选 key


m: Movie = {"title": "Dune", "year": 2021}
# m2: Movie = {"title": "Dune"}            # pyright: "year" is required
# m["foo"]                                  # pyright: "foo" is not a defined key
print(m["title"], m.get("rating", 0.0))  # 运行时它就是普通 dict
# 什么时候用 TypedDict 而不是 dataclass：数据本来就是 dict（JSON 解析出来、要传给只认 dict 的 API）

# ====================================================
# 六、Callable：函数类型，≈ (x: number) => number
# ====================================================


def apply(fn: Callable[[int], int], x: int) -> int:
    return fn(x)


print(apply(lambda v: v * 2, 21))
Handler = Callable[[str, int], None]  # 多参数：[参数类型列表], 返回类型
# Callable[..., int]  任意参数返回 int

# ====================================================
# 七、泛型：3.12+ 的新语法，和 TS 几乎一样
# ====================================================


def first_or[T](items: Sequence[T], default: T) -> T:  # ≈ function firstOr<T>(items: T[], d: T): T
    return items[0] if items else default


print(first_or([1, 2], 0), first_or([], "none"))


class Box[T]:  # ≈ class Box<T>
    def __init__(self, item: T) -> None:
        self.item = item

    def map[U](self, fn: Callable[[T], U]) -> Box[U]:
        return Box(fn(self.item))


b = Box(3).map(lambda n: str(n))  # pyright 推出 Box[str]
print(b.item)
# 3.11 及以前要 from typing import TypeVar; T = TypeVar("T") 再用，老代码里会见到

# ====================================================
# 八、type 语句：复杂类型别名（3.12+），支持递归
# ====================================================
type Json = dict[str, Json] | list[Json] | str | int | float | bool | None  # ≈ type Json = ...


def count_leaves(data: Json) -> int:
    if isinstance(data, dict):
        return sum(count_leaves(v) for v in data.values())
    if isinstance(data, list):
        return sum(count_leaves(v) for v in data)
    return 1


print(count_leaves({"a": [1, 2, {"b": None}], "c": "x"}))  # 4

# ====================================================
# 九、Protocol + runtime_checkable：接口在运行时也能 isinstance
# ====================================================


@runtime_checkable
class HasArea(Protocol):
    def area(self) -> float: ...


class Sq:
    def area(self) -> float:
        return 4.0


print(isinstance(Sq(), HasArea), isinstance("x", HasArea))  # True False
# 不加 @runtime_checkable 的 Protocol 用 isinstance 会直接 TypeError
# 注意：运行时只检查「有没有这个名字的方法」，不检查签名

# ====================================================
# 十、TS → Python 类型速查
# ====================================================
# string/number/boolean      → str / int / float / bool
# T[]                        → list[T]            readonly T[] → Sequence[T]
# [string, number]           → tuple[str, int]
# Record<string, T>          → dict[str, T]       Map<K, V> → dict[K, V]
# T | null | undefined       → T | None
# "a" | "b"                  → Literal["a", "b"]
# interface（给对象字面量）   → TypedDict           interface（给类）→ Protocol
# (x: number) => string      → Callable[[int], str]
# <T>(x: T) => T             → def f[T](x: T) -> T
# type A = ...               → type A = ...（3.12+）
# any                        → Any                unknown → object
# as 断言                    → typing.cast(T, x)  非空断言 x! → assert x is not None
# tsc --strict               → pyright 的 typeCheckingMode = "strict"
