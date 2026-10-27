"""Lesson 08 课堂示例：迭代器、生成器、装饰器、上下文管理器。

运行方式：uv run python -m lesson08.demo
"""

import functools
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager, suppress
from itertools import islice

# ====================================================
# 一、迭代协议：for 循环背后发生了什么
# ====================================================
nums = [1, 2, 3]
it = iter(nums)  # 调 nums.__iter__()，拿到迭代器
print(next(it), next(it), next(it))  # 调 it.__next__()
try:
    next(it)
except StopIteration:  # 耗尽时抛 StopIteration，for 循环靠它知道该停了
    print("耗尽")

# for x in nums: 等价于
# it = iter(nums)
# while True:
#     try: x = next(it)
#     except StopIteration: break
#     ...
# JS 对照：nums[Symbol.iterator]() 返回 { next() { return { value, done } } }，
# done: true 对应 StopIteration

# 可迭代对象（iterable）：有 __iter__，能 for，如 list / dict / str / 文件
# 迭代器（iterator）：有 __next__，是一次性的，走到头就空了


class Countdown:  # 自己实现可迭代对象
    def __init__(self, start: int) -> None:
        self.start = start

    def __iter__(self) -> Iterator[int]:  # 返回一个迭代器；最省事的办法是返回生成器（见下）
        n = self.start
        while n > 0:
            yield n
            n -= 1


print(list(Countdown(3)))

# ====================================================
# 二、生成器：带 yield 的函数，惰性产出，≈ function*
# ====================================================


def squares(n: int) -> Iterator[int]:
    print("  开始")
    for i in range(n):
        print(f"  产出 {i}")
        yield i * i  # 执行到这暂停，把值交出去；下次 next 从这继续
    print("  结束")


gen = squares(3)
print(type(gen).__name__)  # generator；调用函数时一行都没执行！
print(next(gen))  # 现在才跑到第一个 yield
print(list(gen))  # 继续跑完剩下的


def fib() -> Iterator[int]:  # 无限序列：惰性所以可以无限
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


print(list(islice(fib(), 10)))  # islice 取前 10 个，不会死循环

# 生成器表达式：推导式的括号换成圆括号，不建列表
total = sum(x * x for x in range(1_000_000))  # 不会在内存里放一百万个数
print(total)
# Lesson 03 的 any(n > 5 for n in nums) 括号里就是生成器表达式


def read_lines(path: str) -> Iterator[str]:  # 典型用法：大文件逐行处理
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")


def flatten(nested: list[list[int]]) -> Iterator[int]:
    for row in nested:
        yield from row  # 把另一个可迭代对象的元素逐个产出，≈ yield*


print(list(flatten([[1, 2], [3]])))

# 生成器是一次性的：
g = (x for x in range(3))
print(list(g), list(g))  # [0, 1, 2] []  —— 第二次是空的！要重来就再调一次函数

# ====================================================
# 三、闭包回顾：函数可以记住定义时的环境（Lesson 02 讲过 nonlocal）
# ====================================================


def make_multiplier(k: int) -> Callable[[int], int]:
    def multiply(x: int) -> int:
        return x * k  # k 被「捕获」

    return multiply


triple = make_multiplier(3)
print(triple(10))

# ====================================================
# 四、装饰器：接收函数、返回函数的函数。@ 只是语法糖
# ====================================================


def log_calls[**P, R](fn: Callable[P, R]) -> Callable[P, R]:  # P 是参数规格，R 是返回类型
    @functools.wraps(
        fn
    )  # 把 fn 的 __name__ / __doc__ 抄到 wrapper 上，不写的话函数名会变成 wrapper
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"-> {fn.__name__}{args}")
        result = fn(*args, **kwargs)  # Lesson 02 的 *args / **kwargs 原样透传
        print(f"<- {result!r}")
        return result

    return wrapper


@log_calls  # 等价于：add = log_calls(add)，在定义时执行一次
def add(a: int, b: int) -> int:
    """加法。"""
    return a + b


print(add(1, 2))
print(add.__name__, add.__doc__)  # 有 wraps 才是 'add' / '加法。'


# 带参数的装饰器：多一层函数，先收参数，再收函数
def retry(times: int) -> Callable[[Callable[..., int]], Callable[..., int]]:
    def decorator(fn: Callable[..., int]) -> Callable[..., int]:
        @functools.wraps(fn)
        def wrapper(*args: object, **kwargs: object) -> int:
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except ValueError as e:
                    print(f"  第 {attempt} 次失败：{e}")
            raise RuntimeError(f"{fn.__name__} 重试 {times} 次仍失败")

        return wrapper

    return decorator


calls = 0


@retry(times=3)  # 等价于：flaky = retry(times=3)(flaky)
def flaky() -> int:
    global calls
    calls += 1
    if calls < 3:
        raise ValueError("还没好")
    return calls


print(flaky())


# 标准库自带的常用装饰器
@functools.cache  # 缓存结果，≈ memoize；要限制条数用 functools.lru_cache(maxsize=128)
def slow_fib(n: int) -> int:
    return n if n < 2 else slow_fib(n - 1) + slow_fib(n - 2)


print(slow_fib(80))  # 没缓存要跑几分钟

# 装饰器也能叠：从下往上应用
# @a
# @b
# def f(): ...     等价于 f = a(b(f))

# 对照 NestJS：@Controller() / @Get() / @Injectable() 也是「定义时执行、拿到类或方法、
# 登记或改造它」。区别：TS 装饰器是语言提案 + reflect-metadata，Python 的装饰器就是普通函数，
# 没有任何魔法，你随时可以手动写 f = deco(f)。Lesson 06 的 @property / @dataclass /
# @classmethod 都是装饰器。

# ====================================================
# 五、上下文管理器：Lesson 04 Q&A 讲过 __enter__ / __exit__，这里讲更简的写法
# ====================================================


class Timer:  # 类写法
    def __enter__(self) -> Timer:
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.elapsed = time.perf_counter() - self.start


with Timer() as t:
    sum(range(100_000))
print(f"{t.elapsed:.6f}s")


@contextmanager  # 生成器写法：yield 之前 = __enter__，之后 = __exit__
def timer(label: str) -> Iterator[None]:
    start = time.perf_counter()
    try:
        yield  # 这里把控制权交给 with 块
    finally:
        print(f"{label}: {time.perf_counter() - start:.6f}s")


with timer("求和"):
    sum(range(100_000))

# 这就是装饰器 + 生成器的合体：contextmanager 是装饰器，被装饰的是生成器函数

with suppress(FileNotFoundError):  # 标准库：忽略指定异常，≈ try/except: pass
    open("不存在.txt")
print("没炸")

# 多个 with 可以写在一行：with open(a) as fa, open(b) as fb:
