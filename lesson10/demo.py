"""Lesson 10 课堂示例：asyncio。对照 Node 的事件循环。

运行方式：uv run python -m lesson10.demo
"""

import asyncio
import time
from collections.abc import AsyncIterator

import httpx

# ====================================================
# 一、协程是惰性的；await 交出控制权；asyncio.run 启动事件循环
# ====================================================


async def fetch(name: str, delay: float) -> str:  # async def 定义协程函数，≈ async function
    print(f"  {name} 开始")
    await asyncio.sleep(delay)  # ≈ await new Promise(r => setTimeout(r, delay*1000))
    print(f"  {name} 结束")
    return name.upper()


coro = fetch("a", 0.1)
print(type(coro).__name__)  # coroutine：调用时一行都没执行（和 Lesson 08 生成器一样惰性）
# Node 的 async 函数调用时会立刻执行到第一个 await；Python 不会，必须 await 它或交给事件循环


async def main_basic() -> None:
    result = await coro  # 现在才执行
    print(result)


asyncio.run(main_basic())  # Node 有隐式的事件循环，Python 必须显式启动一次，整个程序一个入口
# 不能在已运行的循环里再 asyncio.run；也不能在普通函数里 await

# ====================================================
# 二、并发：gather ≈ Promise.all；create_task ≈ 「先发出去不等」
# ====================================================


async def main_concurrent() -> None:
    start = time.perf_counter()
    results = await asyncio.gather(  # 同时跑，总耗时 ≈ 最慢的那个，≈ Promise.all
        fetch("a", 0.2),
        fetch("b", 0.2),
        fetch("c", 0.2),
    )
    print(results, f"{time.perf_counter() - start:.2f}s")  # ['A','B','C'] 0.20s，顺序和传入一致

    # 串行写法对比：三个 await 挨个等，0.6s
    # for n in "abc": await fetch(n, 0.2)

    task = asyncio.create_task(fetch("bg", 0.1))  # 立刻开始跑，≈ 调用 async 函数不 await
    print("  任务已发出，先干别的")
    await asyncio.sleep(0.05)
    print("  现在等它：", await task)  # ≈ await promise

    # 一个失败 gather 整体抛出（和 Promise.all 一样）
    # 要「全部结束不管成败」用 return_exceptions=True，≈ Promise.allSettled
    results2 = await asyncio.gather(
        fetch("x", 0.01), asyncio.sleep(0.01, result="ok"), return_exceptions=True
    )
    print(results2)


asyncio.run(main_concurrent())

# ====================================================
# 三、超时、并发上限、队列
# ====================================================


async def main_control() -> None:
    try:
        async with asyncio.timeout(0.1):  # 3.11+；≈ Promise.race([p, timeoutPromise])
            await fetch("slow", 1.0)
    except TimeoutError:
        print("  超时了")

    sem = asyncio.Semaphore(2)  # 最多 2 个同时跑，≈ p-limit

    async def limited(name: str) -> str:
        async with sem:
            return await fetch(name, 0.1)

    start = time.perf_counter()
    await asyncio.gather(*(limited(n) for n in "abcd"))  # 4 个任务，2 个一批，≈ 0.2s
    print(f"  限流后 {time.perf_counter() - start:.2f}s")

    queue: asyncio.Queue[int] = asyncio.Queue()  # 生产者 / 消费者

    async def worker(wid: int) -> None:
        while True:
            item = await queue.get()
            await asyncio.sleep(0.01)
            print(f"  worker{wid} 处理 {item}")
            queue.task_done()

    workers = [asyncio.create_task(worker(i)) for i in range(2)]
    for i in range(4):
        queue.put_nowait(i)
    await queue.join()  # 等所有 item 被 task_done
    for w in workers:
        w.cancel()  # 取消无限循环的 worker


asyncio.run(main_control())

# ====================================================
# 四、异步迭代与异步上下文管理器
# ====================================================


async def ticker(n: int) -> AsyncIterator[int]:  # async 生成器，≈ async function*
    for i in range(n):
        await asyncio.sleep(0.01)
        yield i


async def main_async_for() -> None:
    async for i in ticker(3):  # ≈ for await (const i of ticker())
        print("  tick", i)
    # async with 对应 __aenter__ / __aexit__，httpx.AsyncClient 就是（见下）


asyncio.run(main_async_for())

# ====================================================
# 五、真实世界：httpx 发 HTTP 请求（≈ fetch / axios）
# ====================================================


def fake_api(request: httpx.Request) -> httpx.Response:  # 为了离线演示，用 MockTransport 假装服务器
    return httpx.Response(200, json={"path": request.url.path})


async def main_http() -> None:
    async with httpx.AsyncClient(transport=httpx.MockTransport(fake_api)) as client:
        # 真实用法：async with httpx.AsyncClient() as client: r = await client.get("https://...")
        responses = await asyncio.gather(*(client.get(f"https://x/{i}") for i in range(3)))
        print([r.json()["path"] for r in responses])
        r = await client.get("https://x/one")
        r.raise_for_status()  # 非 2xx 抛异常
        # r.status_code / r.json() / r.text 和 fetch 的 Response 类似


asyncio.run(main_http())
# httpx 也有同步版 httpx.get(...)，脚本里不需要并发时直接用同步的，别为了 async 而 async

# ====================================================
# 六、阻塞代码会卡住整个循环；CPU 密集 / 同步库用 to_thread
# ====================================================


def blocking_io() -> str:
    time.sleep(0.2)  # 同步 sleep：整个事件循环停 0.2s，其他协程全卡住。≈ 在 Node 里跑 while 死循环
    return "done"


async def main_thread() -> None:
    start = time.perf_counter()
    results = await asyncio.gather(
        asyncio.to_thread(blocking_io),  # 丢到线程池，循环不卡，≈ worker_threads 但简单得多
        asyncio.to_thread(blocking_io),
        fetch("async", 0.2),
    )
    print(results, f"{time.perf_counter() - start:.2f}s")  # ≈ 0.2s 而不是 0.6s


asyncio.run(main_thread())

# 和 Node 的核心差异总结：
#   1. 没有隐式事件循环：asyncio.run() 显式启动，整个程序一个入口
#   2. 协程调用时不执行，必须 await / create_task；
#      忘了 await 会有 RuntimeWarning: coroutine was never awaited
#   3. 同步和异步是两套 API：time.sleep vs asyncio.sleep，open vs aiofiles，
#      requests vs httpx.AsyncClient
#   4. Python 有 GIL：多线程不能并行跑纯 Python 计算；IO 密集用 asyncio / 线程，CPU 密集用多进程
#   5. 大多数脚本根本不需要 async；只有「同时等很多 IO」时才值得
