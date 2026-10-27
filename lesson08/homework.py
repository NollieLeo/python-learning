"""Lesson 08 作业：迭代器、生成器、装饰器、上下文管理器

规则同上：只改 TODO，uv run pytest lesson08 全绿即完成。pyright 也要 0 errors。
"""

import functools
import os
import time
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager


# ---------- 作业 1：生成器 ----------
def countdown(n: int) -> Iterator[int]:
    """从 n 数到 1：list(countdown(3)) -> [3, 2, 1]；countdown(0) 什么都不产出。"""
    yield from range(n, 0, -1)


def chunked[T](items: Iterable[T], size: int) -> Iterator[list[T]]:
    """按 size 分块：list(chunked([1,2,3,4,5], 2)) -> [[1,2],[3,4],[5]]
    必须是惰性的：items 可以是无限生成器，测试会用 islice 只取前几块。
    提示：攒一个 buf 列表，满了就 yield 并清空；循环结束后 buf 非空也要 yield。
    """
    temp: list[T] = []
    for item in items:
        if len(temp) == size:
            yield temp
            temp = []
        temp.append(item)
    if temp:
        yield temp


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def primes() -> Iterator[int]:
    """无限素数生成器：2, 3, 5, 7, 11, ...  测试用 islice 取前 10 个。"""
    n = 2
    while True:
        if is_prime(n):
            yield n
        n += 1


# ---------- 作业 2：可迭代的类 ----------
class Grid:
    """二维网格坐标。
    list(Grid(2, 2)) -> [(0, 0), (0, 1), (1, 0), (1, 1)]   先行后列
    len(Grid(2, 3)) -> 6
    可以被遍历多次（每次 for 都重新开始，不像生成器一次性）。
    提示：__iter__ 里写 yield，或者返回一个生成器表达式。
    """

    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols

    def __iter__(self) -> Iterator[tuple[int, int]]:
        for x in range(self.rows):
            for y in range(self.cols):
                yield x, y

    def __len__(self) -> int:
        return self.cols * self.rows


# ---------- 作业 3：装饰器 ----------
def count_calls[**P, R](fn: Callable[P, R]) -> Callable[P, R]:
    """记录函数被调用的次数，存在 wrapper.calls 上；保留原函数名（functools.wraps）。
    @count_calls
    def f(): ...
    f(); f(); f.calls -> 2; f.__name__ -> "f"
    提示：函数对象可以随便挂属性：wrapper.calls = 0；每次调用 +1。
    pyright 对动态属性会报错，这一处允许写 # type: ignore[attr-defined]。
    """

    @functools.wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        wrapper.calls += 1  # type: ignore[attr-defined]
        return fn(*args, **kwargs)

    wrapper.calls = 0  # type: ignore[attr-defined]
    return wrapper


def retry(
    times: int, exceptions: tuple[type[Exception], ...] = (Exception,)
) -> Callable[[Callable[..., object]], Callable[..., object]]:
    """带参数的装饰器：失败就重试，最多 times 次；全部失败则把最后一次的异常原样抛出。
    只重试 exceptions 里列的异常类型，其他异常直接抛。
    @retry(times=3, exceptions=(ValueError,))
    def f(): ...
    """

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise

        return wrapper

    return decorator


# ---------- 作业 4：上下文管理器 ----------
@contextmanager
def temp_env(key: str, value: str) -> Iterator[None]:
    """临时设置环境变量，退出 with 后恢复原值（原来没有就删掉）。即使 with 块里抛异常也要恢复。
    with temp_env("MODE", "test"):
        os.environ["MODE"] == "test"
    提示：old = os.environ.get(key)；finally 里恢复。
    """
    old = os.environ.get(key)
    try:
        os.environ[key] = value
        yield
    finally:
        if old is not None:
            os.environ[key] = old
        else:
            del os.environ[key]


class Stopwatch:
    """类写法的上下文管理器。
    with Stopwatch() as sw:
        ...
    sw.elapsed -> 秒数（float, > 0）
    with 块里抛的异常不能被吞掉。
    提示：time.perf_counter()。
    """

    def __enter__(self) -> Stopwatch:
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args) -> None:
        self.elapsed = time.perf_counter() - self.start


# ---------- 作业 5：把三样东西用在一起 ----------
def read_numbers(lines: Iterable[str]) -> Iterator[int]:
    """从文本行里惰性产出整数，跳过空行和非数字行。
    list(read_numbers(["1", "", "x", " 42 "])) -> [1, 42]
    提示：生成器 + Lesson 04 的 safe_int 思路（try/except ValueError）。
    """
    for line in lines:
        try:
            num = int(line)
            yield num
        except ValueError:
            pass


# ---------- 作业 6（思考题，写注释回答即可）----------
# 先猜输出，再运行验证：
#
# def gen():
#     print("start")
#     yield 1
#     print("end")


# g = gen()
# print("created")
# print(next(g))
# print(list(g))
# print(list(g))
#
# 你的猜测（打印顺序和每行内容）：
# created
# start 1
# end []
# []
# 实际结果：
# created
# start 1 end
# []
# []
# 解释：g = gen() 只是创建生成器对象函数题并不会执行，next(g)会进入函数体，先跑start然后yield 1交出
# 去1，然后暂停掉生成器，当list(g)跑的时候，会触发剩余的end打印，期间没有新的yield所以收集到了[]空的
# list，第二次list(g)的时候，由于生成器已经执行完了，函数体不会重新走，所以打印了[]
# 第二问：把 count_calls 里的 @functools.wraps(fn) 删掉，f.__name__ 会变成什么？为什么？
# 回答：会变成wrapper，因为@functools.wraps(fn)会把 __name__ / __doc__ 抄到wrapper上
#


QUESTIONS = """
（在这里写你学习过程中的疑问）
"""
