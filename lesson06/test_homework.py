"""自动检查，运行：uv run pytest lesson06"""

import math
from dataclasses import FrozenInstanceError

import pytest

from lesson06.homework import (
    Account,
    Celsius,
    Circle,
    InsufficientFunds,
    Point,
    Shape,
    Square,
    Stack,
    User,
    serialize_all,
    total_area,
)


def test_account_basic():
    acc = Account("kaimin")
    assert acc.balance == 0
    acc.deposit(100)
    acc.withdraw(30)
    assert acc.balance == 70
    assert repr(acc) == "Account(owner='kaimin', balance=70)"


def test_account_errors():
    acc = Account("kaimin", 10)
    with pytest.raises(InsufficientFunds) as info:
        acc.withdraw(20)
    assert str(info.value) == "balance 10 < 20"
    assert info.value.balance == 10
    assert info.value.amount == 20
    assert isinstance(info.value, ValueError)
    with pytest.raises(ValueError, match="amount must be positive"):
        acc.deposit(0)
    with pytest.raises(ValueError, match="amount must be positive"):
        acc.withdraw(-1)
    assert acc.balance == 10  # 失败的操作不能改余额


def test_point():
    assert Point(1, 2) + Point(3, 4) == Point(4, 6)
    assert Point(3, 4).distance_to(Point(0, 0)) == 5.0
    assert len({Point(1, 2), Point(1, 2)}) == 1
    with pytest.raises(FrozenInstanceError):  # frozen：不能赋值
        Point(1, 2).x = 9  # type: ignore[misc]


def test_celsius():
    t = Celsius(25)
    assert t.value == 25
    assert t.fahrenheit == 77.0
    t.value = 30
    assert t.value == 30
    t.fahrenheit = 212
    assert t.value == 100
    with pytest.raises(ValueError, match="below absolute zero"):
        t.value = -300


def test_shapes():
    c, s = Circle(1), Square(2)
    assert c.area() == pytest.approx(math.pi)
    assert s.area() == 4
    assert c.describe() == "circle: 3.14"
    assert s.describe() == "square: 4.00"
    assert sorted([s, c]) == [c, s]  # 按面积
    assert total_area([c, s]) == pytest.approx(math.pi + 4)
    with pytest.raises(TypeError):
        Shape()  # type: ignore[abstract]


def test_serializable():
    assert User("kaimin", 28).to_dict() == {"name": "kaimin", "age": 28}
    assert serialize_all([User("a", 1), User("b", 2)]) == [
        {"name": "a", "age": 1},
        {"name": "b", "age": 2},
    ]


def test_stack():
    s = Stack()
    assert not s
    assert len(s) == 0
    s.push(1)
    s.push(2)
    assert s
    assert len(s) == 2
    assert s.peek() == 2
    assert 2 in s
    assert 3 not in s
    assert list(s) == [1, 2]
    assert repr(s) == "Stack([1, 2])"
    assert s.pop() == 2
    assert s.pop() == 1
    with pytest.raises(IndexError, match="pop from empty stack"):
        s.pop()
    with pytest.raises(IndexError):
        s.peek()
