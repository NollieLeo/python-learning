"""自动检查，运行：uv run pytest lesson02"""

import pytest

from lesson02.homework import apply_n_times, average, first_negative, fizzbuzz, greet


def test_fizzbuzz():
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
    assert fizzbuzz(15)[-1] == "FizzBuzz"
    assert fizzbuzz(0) == []


def test_average():
    assert average(1, 2, 3) == 2.0
    assert average(1, 2) == 1.5
    assert average(1, 2, 2, precision=3) == 1.667
    assert average() == 0.0


def test_greet():
    assert greet("kaimin") == "你好，kaimin！"
    assert greet("kaimin", "早上好") == "早上好，kaimin！"
    assert greet("kaimin", punctuation=".") == "你好，kaimin."
    with pytest.raises(TypeError):
        greet("a", "b", "c")  # type: ignore[misc]


def test_first_negative():
    assert first_negative([3, -1, -5]) == -1
    assert first_negative([1, 2]) is None
    assert first_negative([]) is None


def test_apply_n_times():
    assert apply_n_times(lambda v: v * 2, 1, 3) == 8
    assert apply_n_times(str.upper, "a", 1) == "A"
    assert apply_n_times(lambda v: v + 1, 0, 0) == 0
