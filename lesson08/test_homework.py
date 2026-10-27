"""自动检查，运行：uv run pytest lesson08"""

import os
import subprocess
import sys
from itertools import count, islice
from pathlib import Path

import pytest

from lesson08.homework import (
    Grid,
    Stopwatch,
    chunked,
    count_calls,
    countdown,
    primes,
    read_numbers,
    retry,
    temp_env,
)


def test_countdown():
    assert list(countdown(3)) == [3, 2, 1]
    assert list(countdown(0)) == []


def test_chunked_is_lazy():
    assert list(chunked([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    assert list(chunked([], 3)) == []
    # count() 是无限的，不惰性会卡死
    assert list(islice(chunked(count(), 3), 2)) == [[0, 1, 2], [3, 4, 5]]


def test_primes():
    assert list(islice(primes(), 10)) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]


def test_grid():
    g = Grid(2, 2)
    assert list(g) == [(0, 0), (0, 1), (1, 0), (1, 1)]
    assert list(g) == [(0, 0), (0, 1), (1, 0), (1, 1)]  # 第二次遍历仍然有
    assert len(Grid(2, 3)) == 6


def test_count_calls():
    @count_calls
    def f(x: int) -> int:
        """doc"""
        return x * 2

    assert f(1) == 2
    assert f(2) == 4
    assert f.calls == 2  # type: ignore[attr-defined]
    assert f.__name__ == "f"
    assert f.__doc__ == "doc"


def test_retry():
    attempts: list[int] = []

    @retry(times=3, exceptions=(ValueError,))
    def flaky() -> str:
        attempts.append(1)
        if len(attempts) < 3:
            raise ValueError("not yet")
        return "ok"

    assert flaky() == "ok"
    assert len(attempts) == 3

    @retry(times=2, exceptions=(ValueError,))
    def always_fails() -> None:
        raise ValueError("boom")

    with pytest.raises(ValueError, match="boom"):
        always_fails()

    @retry(times=5, exceptions=(ValueError,))
    def wrong_kind() -> None:
        raise KeyError("not retried")

    with pytest.raises(KeyError):  # 不在列表里的异常不重试，直接抛
        wrong_kind()


def test_temp_env():
    os.environ.pop("L08_MODE", None)
    with temp_env("L08_MODE", "test"):
        assert os.environ["L08_MODE"] == "test"
    assert "L08_MODE" not in os.environ

    os.environ["L08_MODE"] = "orig"
    with pytest.raises(RuntimeError):
        with temp_env("L08_MODE", "tmp"):
            raise RuntimeError("inside")
    assert os.environ["L08_MODE"] == "orig"  # 异常后也恢复
    del os.environ["L08_MODE"]


def test_stopwatch():
    with Stopwatch() as sw:
        sum(range(10_000))
    assert sw.elapsed > 0
    with pytest.raises(ZeroDivisionError):  # 异常不能被吞
        with Stopwatch():
            _ = 1 / 0


def test_read_numbers():
    assert list(read_numbers(["1", "", "x", " 42 "])) == [1, 42]
    gen = read_numbers(iter(["7"]))
    assert next(gen) == 7  # 是生成器，不是列表


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
