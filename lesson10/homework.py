"""Lesson 10 作业：asyncio

规则：只改 TODO，uv run pytest lesson10 全绿（含 pyright）。测试里用 asyncio.run 跑你的协程。
所有「网络请求」都用注入的 fetch 函数模拟，不要真的联网。
"""

import asyncio  # noqa: F401 —— 每道题都要用，写上后把 noqa 删掉
from collections.abc import AsyncIterator, Awaitable, Callable, Iterable


# ---------- 作业 1：并发拉取，保持顺序 ----------
async def fetch_all(urls: list[str], fetch: Callable[[str], Awaitable[str]]) -> list[str]:
    """并发调用 fetch(url)，结果顺序与 urls 一致。
    提示：asyncio.gather(*(...))。测试会检查总耗时 ≈ 单个耗时而不是累加。
    """
    raise NotImplementedError  # TODO


# ---------- 作业 2：并发上限 ----------
async def fetch_all_limited(
    urls: list[str], fetch: Callable[[str], Awaitable[str]], limit: int
) -> list[str]:
    """同上，但同一时刻最多 limit 个 fetch 在跑。测试会统计峰值并发数。
    提示：asyncio.Semaphore(limit) + async with。
    """
    raise NotImplementedError  # TODO


# ---------- 作业 3：超时兜底 ----------
async def with_timeout[T](aw: Awaitable[T], seconds: float, default: T) -> T:
    """等 aw 最多 seconds 秒，超时返回 default 而不是抛异常。
    提示：asyncio.wait_for(aw, seconds)，接 TimeoutError。
    """
    raise NotImplementedError  # TODO


# ---------- 作业 4：异步重试 ----------
async def retry_async[T](fn: Callable[[], Awaitable[T]], times: int, delay: float = 0) -> T:
    """调用 fn()，失败就 await asyncio.sleep(delay) 后重试，最多 times 次；全失败抛最后的异常。
    Lesson 08 的 retry 的 async 版。
    """
    raise NotImplementedError  # TODO


# ---------- 作业 5：生产者 / 消费者 ----------
async def process_with_workers[T, R](
    items: Iterable[T], worker: Callable[[T], Awaitable[R]], n_workers: int
) -> list[R]:
    """n_workers 个协程从 asyncio.Queue 取 item 调 worker，返回所有结果。
    顺序不限，测试排序后比较。
    提示：queue.put_nowait 全部放入；worker 协程 while True: await queue.get() ...
          queue.task_done()；await queue.join() 后 cancel 掉 workers。结果收到一个共享 list 里。
    """
    raise NotImplementedError  # TODO


# ---------- 作业 6：异步生成器 ----------
async def countdown(n: int, interval: float) -> AsyncIterator[int]:
    """每隔 interval 秒产出一个数：n, n-1, ..., 1。测试用 async for 收集。"""
    raise NotImplementedError  # TODO
    yield 0  # 让函数成为 async 生成器；写完删掉这行


# ---------- 作业 7：把阻塞函数变成不阻塞 ----------
async def run_blocking[T](fn: Callable[[], T]) -> T:
    """fn 是同步阻塞函数（比如 time.sleep），在线程里跑它，不卡事件循环。
    测试会同时跑两个 run_blocking(睡 0.2s)，期望总耗时 < 0.35s。
    提示：asyncio.to_thread。
    """
    raise NotImplementedError  # TODO


# ---------- 作业 8（思考题，写注释回答即可）----------
# 1. 下面代码会打印什么？会有什么警告？为什么？
#       async def hello():
#           print("hi")
#       async def main():
#           hello()
#       asyncio.run(main())
#
# 2. 在协程里写 time.sleep(1) 和 await asyncio.sleep(1) 的区别是什么？对其他协程有什么影响？
#
# 3. Node 里调用一个 async 函数会立刻开始执行到第一个 await；Python 不会。
#    那 Python 里「先发出去、稍后再等」的写法是什么？
#
# 回答：
# 1.
# 2.
# 3.


QUESTIONS = """
（在这里写你学习过程中的疑问）
"""
