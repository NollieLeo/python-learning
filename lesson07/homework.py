"""Lesson 07 作业：类型注解

规则：只改 TODO，uv run pytest lesson07 全绿即完成。
这课的测试里有一条会运行 pyright 检查本文件，类型写错也算挂。
手动查：uv run pyright lesson07/homework.py
"""

from collections.abc import Callable, Iterable, Sequence
from typing import Literal, NotRequired, Protocol, TypedDict, runtime_checkable


# ---------- 作业 1：Optional 与收窄 ----------
def safe_div(a: float, b: float) -> float | None:
    """b 为 0 返回 None，否则返回 a / b。"""
    if not b:
        return None
    return a / b


def div_or_zero(a: float, b: float) -> float:
    """调用 safe_div，结果是 None 就返回 0.0。要求：不能用 Any / cast，靠收窄让 pyright 通过。"""
    result = safe_div(a, b)
    if result is None:
        return 0.0
    return result


# ---------- 作业 2：泛型函数（3.12+ 语法） ----------
def last[T](items: Sequence[T]) -> T | None:  # noqa: UP047 —— 这里故意用新语法
    """返回最后一个元素，空序列返回 None。
    last([1, 2, 3]) -> 3        pyright 推断为 int | None
    last("abc") -> "c"          str 也是 Sequence[str]
    last([]) -> None
    """
    if not items:
        return None
    return items[-1]


def pairwise[T](items: Sequence[T]) -> list[tuple[T, T]]:  # noqa: UP047
    """相邻两两配对：pairwise([1, 2, 3]) -> [(1, 2), (2, 3)]；少于 2 个返回 []。
    提示：zip(items, items[1:])。
    """
    return [*zip(items, items[1:], strict=False)]


# ---------- 作业 3：TypedDict ----------
class Movie(TypedDict):
    title: str
    year: int
    rating: NotRequired[float]


def describe_movie(m: Movie) -> str:
    """describe_movie({"title": "Dune", "year": 2021}) -> "Dune (2021)"
    有 rating -> "Dune (2021) ★8.1"（rating 保留 1 位小数）
    提示：m.get("rating") 收窄后再用。
    """
    rating = m.get("rating")
    result = f"{m['title']} ({m['year']})"
    if rating is None:
        return result
    return f"{result} ★{rating:.1f}"


# ---------- 作业 4：Literal ----------
type Order = Literal["asc", "desc"]


def sort_movies(movies: list[Movie], order: Order = "asc") -> list[Movie]:
    """按 year 排序，返回新列表，order 决定升降。"""
    is_desc = order == "desc"
    return sorted(movies, key=lambda m: m.get("year"), reverse=is_desc)


# ---------- 作业 5：Callable ----------
def compose(f: Callable[[int], int], g: Callable[[int], int]) -> Callable[[int], int]:
    """返回一个新函数 h，h(x) == g(f(x))。
    compose(lambda x: x + 1, lambda x: x * 2)(3) -> 8
    """
    return lambda x: g(f(x))


# ---------- 作业 6：Protocol + runtime_checkable ----------
@runtime_checkable
class Named(Protocol):
    name: str


class Dog:
    def __init__(self, name: str) -> None:
        self.name = name


class Rock:
    pass


def names_of(items: Iterable[object]) -> list[str]:
    """从一堆任意对象里挑出符合 Named 协议的，返回它们的 name。
    names_of([Dog("rex"), Rock(), Dog("ace")]) -> ["rex", "ace"]
    提示：isinstance(item, Named)，收窄后 item.name 才能通过 pyright。
    """
    return [item.name for item in items if isinstance(item, Named)]


# ---------- 作业 7：递归类型别名 ----------
type Json = dict[str, Json] | list[Json] | str | int | float | bool | None


def max_depth(data: Json) -> int:
    """嵌套深度。标量为 0，空容器为 1，容器为 1 + 子元素最大深度。
    max_depth(1) -> 0;  max_depth([]) -> 1;  max_depth([1, [2]]) -> 2
    max_depth({"a": {"b": [1]}}) -> 3
    """
    if isinstance(data, dict):
        if not data:
            return 1
        return 1 + max(max_depth(item) for item in data.values())
    elif isinstance(data, list):
        if not data:
            return 1
        return 1 + max(max_depth(item) for item in data)
    return 0


# ---------- 作业 8：修类型（下面的函数逻辑是对的，注解是错的，pyright 会报错） ----------
# 任务：只改注解，不改函数体，让 uv run pyright lesson07/homework.py 变成 0 errors。
# 每处改完在旁边注释一句原因。


def mean(
    xs: list[int],
) -> float:  # 原因：/ 永远产生 float（Lesson 01），int 列表的平均数也可能是 2.5
    return sum(xs) / len(xs)


def shout(text: str | None) -> str:  # 原因：签名允许 None，函数体就必须处理 None，这里用三元收窄
    return (text.upper() if text else "") + "!"


def head[T](xs: Sequence[T]) -> T:  # 原因：元素是什么类型就返回什么类型，用泛型而不是写死 str；
    return xs[
        0
    ]  # 返回值不可能是 None（空序列抛 IndexError），所以不标 | None；参数只读且需下标，用 Sequence


# ---------- 作业 9（思考题，写注释回答即可）----------
# 1. 下面两个签名的区别是什么？什么时候该用哪个？
#       def f(xs: list[int]) -> None
#       def g(xs: Iterable[int]) -> None
# 2. TypedDict 和 dataclass 都能表示「有固定字段的记录」，各自的运行时对象是什么？
#    从 JSON 解析出来的数据你会用哪个？
# 3. Protocol 和 Lesson 06 的 ABC 在「isinstance」这件事上的区别是什么？
#
# 回答：
# 1. 参数只是 for 遍历用 Iterable，谁都能传；需要下标、len、切片用 Sequence；要往里 append 或明确要
#  list 的方法才用 list。返回值反过来，标具体的 list
# 2. TypedDict 的运行时对象就是普通 dict，type(m) 是 dict，不是「没有」。
#    dataclass 的运行时对象是那个类的实例，能点访问、能挂方法
# 3. ABC 的 isinstance 查继承关系，天生可用；Protocol 的 isinstance 要加 @runtime_checkable 才能用
# ，查的是有没有那些名字


QUESTIONS = """
（在这里写你学习过程中的疑问）
"""
