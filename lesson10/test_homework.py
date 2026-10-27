"""自动检查，运行：uv run pytest lesson10"""

import asyncio
import subprocess
import sys
import time
from pathlib import Path

import pytest

from lesson10.homework import (
    countdown,
    fetch_all,
    fetch_all_limited,
    process_with_workers,
    retry_async,
    run_blocking,
    with_timeout,
)


def make_fetch(delay: float, tracker: dict[str, int] | None = None):
    """返回一个假的异步 fetch：睡 delay 秒后返回 url 大写。tracker 用来统计并发峰值。"""

    async def fetch(url: str) -> str:
        if tracker is not None:
            tracker["now"] += 1
            tracker["peak"] = max(tracker["peak"], tracker["now"])
        await asyncio.sleep(delay)
        if tracker is not None:
            tracker["now"] -= 1
        return url.upper()

    return fetch


def test_fetch_all_is_concurrent_and_ordered():
    start = time.perf_counter()
    result = asyncio.run(fetch_all(["a", "b", "c", "d"], make_fetch(0.1)))
    elapsed = time.perf_counter() - start
    assert result == ["A", "B", "C", "D"]
    assert elapsed < 0.3, f"看起来是串行的：{elapsed:.2f}s"


def test_fetch_all_limited_respects_limit():
    tracker = {"now": 0, "peak": 0}
    result = asyncio.run(
        fetch_all_limited([str(i) for i in range(6)], make_fetch(0.05, tracker), 2)
    )
    assert result == [str(i) for i in range(6)]
    assert tracker["peak"] == 2


def test_with_timeout():
    async def slow() -> str:
        await asyncio.sleep(1)
        return "slow"

    async def quick() -> str:
        return "quick"

    assert asyncio.run(with_timeout(quick(), 0.5, "default")) == "quick"
    start = time.perf_counter()
    assert asyncio.run(with_timeout(slow(), 0.05, "default")) == "default"
    assert time.perf_counter() - start < 0.5


def test_retry_async():
    attempts: list[int] = []

    async def flaky() -> str:
        attempts.append(1)
        if len(attempts) < 3:
            raise ValueError("not yet")
        return "ok"

    assert asyncio.run(retry_async(flaky, times=3)) == "ok"
    assert len(attempts) == 3

    async def always_fails() -> None:
        raise ValueError("boom")

    with pytest.raises(ValueError, match="boom"):
        asyncio.run(retry_async(always_fails, times=2))


def test_process_with_workers():
    async def worker(x: int) -> int:
        await asyncio.sleep(0.02)
        return x * 2

    start = time.perf_counter()
    result = asyncio.run(process_with_workers(range(8), worker, n_workers=4))
    elapsed = time.perf_counter() - start
    assert sorted(result) == [x * 2 for x in range(8)]
    assert elapsed < 0.1, f"4 个 worker 处理 8 个 0.02s 的任务应 ≈ 0.04s，实际 {elapsed:.2f}s"


def test_countdown_async_generator():
    async def collect() -> list[int]:
        return [i async for i in countdown(3, 0.01)]

    assert asyncio.run(collect()) == [3, 2, 1]


def test_run_blocking_does_not_block_loop():
    def blocking() -> str:
        time.sleep(0.2)
        return "done"

    async def main() -> list[str]:
        return list(await asyncio.gather(run_blocking(blocking), run_blocking(blocking)))

    start = time.perf_counter()
    assert asyncio.run(main()) == ["done", "done"]
    assert time.perf_counter() - start < 0.35


@pytest.mark.slow
def test_pyright_clean():
    target = Path(__file__).parent / "homework.py"
    result = subprocess.run(
        [sys.executable, "-m", "pyright", str(target)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert "0 errors" in result.stdout, result.stdout + result.stderr
