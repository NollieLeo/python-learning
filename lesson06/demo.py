"""Lesson 06 课堂示例：面向对象。

运行方式：uv run python -m lesson06.demo
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol

# ====================================================
# 一、最基本的类：__init__ 就是 constructor，self 就是 this（但要显式写）
# ====================================================


class Account:
    bank = "PyBank"  # 类属性：所有实例共享，≈ static

    def __init__(self, owner: str, balance: float = 0) -> None:
        self.owner = owner  # 实例属性：直接赋值就创建，不用先声明
        self.balance = balance

    def deposit(self, amount: float) -> None:  # 每个方法第一个参数都是 self
        self.balance += amount

    def __repr__(self) -> str:  # 调试用的字符串表示，print 和 REPL 都会用它
        return f"Account(owner={self.owner!r}, balance={self.balance})"


acc = Account("kaimin", 100)  # 没有 new
acc.deposit(50)
print(acc, acc.bank, Account.bank)
print(Account.deposit)  # 方法其实是挂在类上的普通函数
Account.deposit(acc, 1)  # acc.deposit(1) 就是这个的语法糖，所以 self 要显式写
print(acc.balance)

# 没有 private 关键字。约定：_name 内部用，__name 会被改名（name mangling），很少用
# 没有重载（overload），一个类里同名方法后者覆盖前者；用默认参数或 *args 代替

# ====================================================
# 二、@property：把方法伪装成属性，相当于 TS 的 get / set
# ====================================================


class Temperature:
    def __init__(self, celsius: float) -> None:
        self._celsius = celsius  # 下划线：内部存储

    @property
    def celsius(self) -> float:  # 读 t.celsius 时调用
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:  # 写 t.celsius = x 时调用
        if value < -273.15:
            raise ValueError("低于绝对零度")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:  # 只读属性：只定义 getter
        return self._celsius * 9 / 5 + 32


t = Temperature(25)
print(t.celsius, t.fahrenheit)  # 不加括号
t.celsius = 30
try:
    t.celsius = -300
except ValueError as e:
    print("拦住了：", e)

# ====================================================
# 三、@dataclass：自动生成 __init__ / __repr__ / __eq__，TS 里「只有字段的 class」就用它
# ====================================================


@dataclass
class Point:
    x: float
    y: float = 0  # 默认值
    tags: list[str] = field(
        default_factory=list
    )  # 可变默认值必须用 default_factory（Lesson 02 的坑）

    def distance_to(self, other: Point) -> float:  # 注解里直接写自己的类名，3.14 起不用加引号
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


p1 = Point(3, 4)
p2 = Point(3, 4)
print(p1)  # Point(x=3, y=4, tags=[])  自动 __repr__
print(p1 == p2)  # True  自动 __eq__ 按字段比较（普通 class 默认比身份）
print(p1.distance_to(Point(0, 0)))


@dataclass(
    frozen=True
)  # 不可变：赋值会 FrozenInstanceError，且自动可哈希（能做 dict key / 进 set）
class Color:
    r: int
    g: int
    b: int


print({Color(255, 0, 0): "red"})

# ====================================================
# 四、继承、super()、抽象基类
# ====================================================


class Shape(ABC):  # ABC = 抽象基类，≈ abstract class
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod  # 子类必须实现，否则实例化时 TypeError
    def area(self) -> float: ...

    def describe(self) -> str:  # 普通方法，子类直接继承
        return f"{self.name}: {self.area():.2f}"


class Circle(Shape):
    def __init__(self, r: float) -> None:
        super().__init__("circle")  # 调父类构造，不传 self
        self.r = r

    def area(self) -> float:
        return 3.14159 * self.r**2


class Rect(Shape):
    def __init__(self, w: float, h: float) -> None:
        super().__init__("rect")
        self.w, self.h = w, h

    def area(self) -> float:
        return self.w * self.h


shapes: list[Shape] = [Circle(1), Rect(2, 3)]
for s in shapes:
    print(s.describe())  # 多态：各自调各自的 area
print(isinstance(shapes[0], Shape), issubclass(Circle, Shape))
try:
    Shape("x")  # type: ignore[abstract]
except TypeError as e:
    print("抽象类不能实例化：", e)

# ====================================================
# 五、魔术方法（dunder）：让自己的对象支持运算符和内置函数
# ====================================================


class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x, self.y = x, y

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def __str__(self) -> str:  # str() / print / f-string 用它；没定义就退回 __repr__
        return f"<{self.x}, {self.y}>"

    def __add__(self, other: Vector) -> Vector:  # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other: object) -> bool:  # v1 == v2
        return isinstance(other, Vector) and (self.x, self.y) == (other.x, other.y)

    def __lt__(self, other: Vector) -> bool:  # v1 < v2，有了它 sorted / min / max 就能用
        return abs(self) < abs(other)

    def __abs__(self) -> float:  # abs(v)
        return (self.x**2 + self.y**2) ** 0.5

    def __len__(self) -> int:  # len(v)；同时决定 bool(v)：len 为 0 就是 False
        return 2

    def __getitem__(self, i: int) -> float:  # v[0]；有了它还能 for 循环和解包
        return (self.x, self.y)[i]


v = Vector(3, 4) + Vector(1, 1)
print(repr(v), str(v), f"{v}")
print(abs(Vector(3, 4)), len(v), v[0], list(v))
print(sorted([Vector(3, 4), Vector(1, 1)]))
x, y = v
print(x, y)

# 常用一览：__init__ 构造  __repr__/__str__ 字符串  __eq__/__lt__ 比较  __hash__
#           __len__ __getitem__ __iter__ __contains__ 容器  __add__ __mul__ 运算
#           __enter__/__exit__ 上下文（Lesson 04）  __call__ 让实例可调用

# ====================================================
# 六、Protocol：结构化类型，这才是 TS interface 的真正对应物
# ====================================================


class Greeter(Protocol):  # 不需要继承它，长得像就算实现（duck typing + 静态检查）
    def greet(self) -> str: ...


class English:
    def greet(self) -> str:
        return "hello"


class Chinese:
    def greet(self) -> str:
        return "你好"


class Dog:
    def bark(self) -> str:
        return "汪"


def greet_all(items: list[Greeter]) -> list[str]:
    return [item.greet() for item in items]


print(greet_all([English(), Chinese()]))  # English/Chinese 没继承 Greeter，照样符合
# greet_all([Dog()])  # 运行时才报 AttributeError；pyright 在编辑器里就会标红

# ABC vs Protocol：ABC 是名义类型（必须继承，≈ TS 的 abstract class / implements）
#                  Protocol 是结构类型（≈ TS interface 的默认行为）。
#                  自己写框架、要求子类必须实现时用 ABC；描述「只要有这个方法就行」用 Protocol

# ====================================================
# 七、@classmethod / @staticmethod
# ====================================================


class User:
    count = 0

    def __init__(self, name: str) -> None:
        self.name = name
        User.count += 1

    @classmethod  # 第一个参数是类本身，常用来做「替代构造函数」
    def from_dict(cls, d: dict) -> User:
        return cls(d["name"])

    @staticmethod  # 不拿 self 也不拿 cls，就是挂在类命名空间里的普通函数
    def is_valid_name(name: str) -> bool:
        return bool(name.strip())


u = User.from_dict({"name": "kaimin"})
print(u.name, User.count, User.is_valid_name(" "))


print(Point(1, 2))
print(Account("k"))
