"""自动检查，运行：uv run pytest lesson07"""

import subprocess
import sys
from pathlib import Path

import pytest

from lesson07.homework import (
    Dog,
    Rock,
    compose,
    describe_movie,
    div_or_zero,
    head,
    last,
    max_depth,
    mean,
    names_of,
    pairwise,
    safe_div,
    shout,
    sort_movies,
)


def test_safe_div():
    assert safe_div(1, 4) == 0.25
    assert safe_div(1, 0) is None
    assert div_or_zero(1, 0) == 0.0
    assert div_or_zero(9, 3) == 3.0


def test_generics():
    assert last([1, 2, 3]) == 3
    assert last("abc") == "c"
    assert last([]) is None
    assert pairwise([1, 2, 3]) == [(1, 2), (2, 3)]
    assert pairwise([1]) == []


def test_typeddict_and_literal():
    dune = {"title": "Dune", "year": 2021}
    blade = {"title": "Blade Runner", "year": 1982, "rating": 8.1}
    assert describe_movie(dune) == "Dune (2021)"
    assert describe_movie(blade) == "Blade Runner (1982) ★8.1"
    assert [m["year"] for m in sort_movies([dune, blade])] == [1982, 2021]
    assert [m["year"] for m in sort_movies([dune, blade], "desc")] == [2021, 1982]


def test_compose():
    assert compose(lambda x: x + 1, lambda x: x * 2)(3) == 8


def test_protocol():
    assert names_of([Dog("rex"), Rock(), Dog("ace"), 42]) == ["rex", "ace"]


def test_max_depth():
    assert max_depth(1) == 0
    assert max_depth([]) == 1
    assert max_depth([1, [2]]) == 2
    assert max_depth({"a": {"b": [1]}}) == 3


def test_fixed_functions_still_work():
    assert mean([1, 2, 3, 4]) == 2.5
    assert shout("hi") == "HI!"
    assert shout(None) == "!"  # None 当作空字符串处理
    assert head(["a", "b"]) == "a"


@pytest.mark.slow
def test_pyright_clean():
    """类型检查也是作业的一部分：homework.py 必须 0 errors。"""
    target = Path(__file__).parent / "homework.py"
    result = subprocess.run(
        [sys.executable, "-m", "pyright", str(target)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert "0 errors" in result.stdout, result.stdout + result.stderr
