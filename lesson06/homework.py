"""Lesson 06 作业：面向对象

规则同上：只改 TODO，不改签名，uv run pytest lesson06 全绿即完成。
"""

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


# ---------- 作业 1：普通类 + 自定义异常 ----------
class InsufficientFunds(ValueError):
    """余额不足。消息格式："balance 10 < 20"，并带 .balance / .amount 属性。"""

    def __init__(self, balance: float, amount: float) -> None:
        super().__init__(f"balance {balance} < {amount}")  # 消息格式和 docstring 完全一致
        self.balance = balance
        self.amount = amount


class Account:
    """银行账户。
    Account("kaimin")            -> balance 0
    Account("kaimin", 100)       -> balance 100
    acc.deposit(50)              -> balance += 50
    amount <= 0                  -> deposit / withdraw 都抛 ValueError("amount must be positive")
    acc.withdraw(30)             -> balance -= 30；不足抛 InsufficientFunds
    repr(acc)                    -> "Account(owner='kaimin', balance=120)"
    """

    def __init__(self, owner: str, balance: float = 0) -> None:
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self.balance:
            raise InsufficientFunds(self.balance, amount)
        self.balance -= amount

    def __repr__(self) -> str:
        return f"Account(owner={self.owner!r}, balance={self.balance})"


# ---------- 作业 2：dataclass ----------
@dataclass(frozen=True)
class Point:
    """不可变的二维点。
    Point(1, 2) + Point(3, 4) -> Point(4, 6)      （实现 __add__）
    Point(3, 4).distance_to(Point(0, 0)) -> 5.0
    Point(1, 2) == Point(1, 2) -> True             （dataclass 自动生成，不用写）
    {Point(1, 2)}                                  （frozen 自动可哈希，不用写）
    """

    x: float
    y: float

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def distance_to(self, other: Point) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


# ---------- 作业 3：property ----------
class Celsius:
    """温度，内部只存摄氏度。
    t = Celsius(25); t.value -> 25; t.fahrenheit -> 77.0
    t.value = 30 -> 允许；t.value = -300 -> ValueError("below absolute zero")
    t.fahrenheit = 212 -> 反算成摄氏存起来，t.value == 100
    提示：@property + @xxx.setter，内部字段叫 _value。
    """

    def __init__(self, value: float) -> None:
        self._value = value

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, set_value: float) -> None:
        if set_value < -273.15:
            raise ValueError("below absolute zero")
        self._value = set_value

    @property
    def fahrenheit(self) -> float:
        return self._value * 1.8 + 32

    @fahrenheit.setter
    def fahrenheit(self, set_value: float) -> None:
        new_value = (set_value - 32) / 1.8
        self.value = new_value


# ---------- 作业 4：抽象基类 + 继承 + 排序 ----------
class Shape(ABC):
    """抽象形状。子类必须实现 area()。
    shape.describe() -> f"{type(self).__name__.lower()}: {self.area():.2f}"   （基类实现一次即可）
    形状之间可以用 < 比较（按面积），这样 sorted(shapes) 就能用。
    """

    @abstractmethod
    def area(self) -> float: ...

    def describe(self) -> str:
        return f"{type(self).__name__.lower()}: {self.area():.2f}"

    def __lt__(self, other: Shape) -> bool:
        return self.area() < other.area()


class Circle(Shape):
    def __init__(self, r: float) -> None:
        self.r = r

    def area(self) -> float:
        return self.r**2 * math.pi


class Square(Shape):
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side * self.side


def total_area(shapes: list[Shape]) -> float:
    """所有形状面积之和。提示：sum + 生成器表达式。"""
    return sum(shape.area() for shape in shapes)


# ---------- 作业 5：Protocol（结构化类型） ----------
class Serializable(Protocol):
    def to_dict(self) -> dict: ...


class User:
    """普通类，不继承 Serializable，但有 to_dict 方法，所以「结构上」符合。
    User("kaimin", 28).to_dict() -> {"name": "kaimin", "age": 28}
    """

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def to_dict(self) -> dict:
        return {"name": self.name, "age": self.age}


def serialize_all(items: list[Serializable]) -> list[dict]:
    """serialize_all([User("a", 1), User("b", 2)])
    -> [{"name": "a", "age": 1}, {"name": "b", "age": 2}]"""
    return [item.to_dict() for item in items]


# ---------- 作业 6：魔术方法让自定义容器像内置类型 ----------
class Stack:
    """栈。
    s = Stack(); s.push(1); s.push(2)
    len(s) -> 2；bool(Stack()) -> False（靠 __len__ 自动得到）
    s.pop() -> 2；空栈 pop 抛 IndexError("pop from empty stack")
    s.peek() -> 栈顶但不弹出；空栈 peek 抛 IndexError 同上
    2 in s -> True（实现 __contains__）
    list(s) -> [1, 2]，从栈底到栈顶（实现 __iter__，提示：return iter(self._items)）
    repr(s) -> "Stack([1, 2])"
    """

    def __init__(self) -> None:
        self._items = []

    def push(self, val: int) -> None:
        self._items.append(val)

    def pop(self) -> int:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> int:
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, item):
        return item in self._items

    def __iter__(self):
        return iter(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items!r})"


# ---------- 作业 7（思考题，写注释回答即可）----------
# 先猜输出，再运行验证：
#
#   class Team:
#       members = []            # 类属性
#       def add(self, name):
#           self.members.append(name)
#
#   a, b = Team(), Team()
#   a.add("x")
#   print(b.members)
#
# 你的猜测：["x"]
# 实际结果：["x"]
# 解释（为什么 b 也有 "x"；要怎么改才对）：
# 代码中的 members = [] 定义在类的主体内，属于类属性（Class Attribute），被 Team 类的所有实例共享。
# 当你执行 a.add("x") 时，append 操作原地修改了这个共享的列表。因为 a 和 b 的 members 指向内存中的同
# 一个列表对象，所以 b.members 也会显示被修改后的结果。
# 要让每个实例拥有独立的列表，必须将 members 放在 __init__ 方法中定义为实例属性
#
# 第二问：print(Point(1, 2)) 和 print(Account("k")) 一个用了自动生成的 __repr__，
# 一个用了你手写的。如果 Account 不写 __repr__，print 会输出什么样的东西？试一下并写下来：
# <lesson06.homework.Account object at 0x104d3e2d0>

QUESTIONS = """
（在这里写你学习过程中的疑问）
"""
