"""被测代码示例：一个小计算模块，配合 test_calc_demo.py 演示 pytest 的各种用法。"""

import json
import logging
import os
from pathlib import Path

log = logging.getLogger(__name__)  # 约定：每个模块一个 logger，名字就是模块名


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("b must not be 0")
    return a / b


def mean(xs: list[float]) -> float:
    if not xs:
        raise ValueError("empty")
    return sum(xs) / len(xs)


def load_scores(path: Path) -> list[float]:
    """从 JSON 文件读分数列表。"""
    log.info("loading %s", path)  # 日志用 % 占位，不要用 f-string（见讲义）
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def greeting() -> str:
    """依赖环境变量和外部输入的函数，测试时需要「替换掉」依赖。"""
    name = os.environ.get("USER_NAME", "stranger")
    return f"hello, {name}"


def fetch_rate(currency: str) -> float:
    """假装去调外部 API。测试里绝不能真的发请求，要 mock 掉。"""
    raise RuntimeError("network unavailable in this demo")


def convert(amount: float, currency: str) -> float:
    return round(amount * fetch_rate(currency), 2)
