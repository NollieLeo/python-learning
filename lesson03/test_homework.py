"""自动检查，运行：uv run pytest lesson03"""

from lesson03.homework import (
    flatten,
    group_by_length,
    invert_dict,
    squares_of_evens,
    top_n,
    unique_sorted,
    word_count,
)


def test_unique_sorted():
    original = [3, 1, 3, 2]
    assert unique_sorted(original) == [1, 2, 3]
    assert original == [3, 1, 3, 2]  # 不能改原列表
    assert unique_sorted([]) == []


def test_word_count():
    assert word_count("a B a") == {"a": 2, "b": 1}
    assert word_count("") == {}
    assert word_count("  x\n y\tx ") == {"x": 2, "y": 1}


def test_invert_dict():
    assert invert_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}
    assert invert_dict({}) == {}


def test_squares_of_evens():
    assert squares_of_evens([1, 2, 3, 4]) == [4, 16]
    assert squares_of_evens([1, 3]) == []


def test_top_n():
    assert top_n({"a": 1, "b": 3, "c": 2}, 2) == [("b", 3), ("c", 2)]
    assert top_n({"a": 1, "b": 1}, 5) == [("a", 1), ("b", 1)]  # 同分保持顺序，n 超长不报错
    assert top_n({}, 3) == []


def test_flatten():
    assert flatten([[1, 2], [], [3]]) == [1, 2, 3]
    assert flatten([]) == []


def test_group_by_length():
    assert group_by_length(["a", "bb", "c"]) == {1: ["a", "c"], 2: ["bb"]}
    assert group_by_length([]) == {}
