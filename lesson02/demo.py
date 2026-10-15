"""Lesson 02 课堂示例：控制流与函数。

运行方式：uv run python lesson02/demo.py
"""

# ====================================================
# 一、条件：没有括号，没有花括号，靠缩进和冒号
# ====================================================
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:  # 是 elif，不是 else if
    grade = "B"
else:
    grade = "C"
print(grade)

# 三元表达式：顺序和 JS 不一样，是「结果 if 条件 else 结果」
label = "及格" if score >= 60 else "不及格"
print(label)

# Python 3.10+ 有 match，类似 switch 但强得多（模式匹配），这里只看最简单用法
match grade:
    case "A" | "B":
        print("优秀")
    case "C":
        print("一般")
    case _:  # 相当于 default
        print("未知")

# ====================================================
# 二、循环：for 是「for of」，没有 C 风格的 for (let i = 0; ...)
# ====================================================
skills = ["ts", "node", "python"]

for skill in skills:  # for (const skill of skills)
    print(skill)

for i in range(3):  # 0, 1, 2 —— range(start, stop, step)，stop 不包含
    print(i)

for i, skill in enumerate(skills):  # skills.entries() / forEach((skill, i) => ...)
    print(i, skill)

names = ["a", "b", "c"]
for name, skill in zip(names, skills, strict=True):  # 同时遍历两个列表；strict=True 长度不等时报错
    print(name, skill)

n = 0
while n < 3:
    n += 1  # 没有 n++，只有 += 1
    if n == 2:
        continue
    print("while", n)

# for ... else：循环没有被 break 打断时执行 else（JS 没有的东西）
for skill in skills:
    if skill == "go":
        print("找到 go")
        break
else:
    print("没找到 go")

# ====================================================
# 三、函数
# ====================================================


def add(a: int, b: int = 10) -> int:
    """默认参数；类型注解只是提示，运行时不检查（和 TS 擦除后一样）。"""
    return a + b


print(add(1))  # 11
print(add(1, 2))  # 3
print(add(b=5, a=1))  # 6 —— 关键字参数，顺序随便。JS 没有这个，要靠对象解构模拟


def no_return():
    pass  # pass 是占位语句，什么都不做；函数没写 return 就返回 None


print(no_return())  # None


def min_max(nums: list[int]) -> tuple[int, int]:
    return min(nums), max(nums)  # 返回多个值其实是返回一个 tuple


lo, hi = min_max([3, 1, 2])  # 解包，相当于 const [lo, hi] = ...
print(lo, hi)


def total(*nums: int, start: int = 0) -> int:
    """*nums 收集所有位置参数成 tuple，相当于 (...nums)。
    * 后面的参数只能用关键字传（keyword-only）。"""
    result = start
    for n in nums:
        result += n
    return result


print(total(1, 2, 3))  # 6
print(total(1, 2, 3, start=100))  # 106
values = [4, 5, 6]
print(total(*values))  # 展开列表传参，相当于 total(...values)


def show(**options: str) -> None:
    """**options 收集所有多余的关键字参数成 dict。"""
    for key, value in options.items():
        print(f"{key}={value}")


show(color="red", size="L")
config = {"color": "blue", "size": "M"}
show(**config)  # 展开 dict 传参，相当于 show({...config}) 但更像是「把对象拆成具名参数」

# lambda：只能写一个表达式，相当于单行箭头函数
double = lambda x: x * 2  # noqa: E731 —— 实际项目里会用 def，这里只是演示
print(double(21))
print(sorted(skills, key=lambda s: len(s)))  # 按长度排序，key 相当于 comparator 的简化版

# ====================================================
# 四、作用域：函数内赋值会创建局部变量
# ====================================================
counter = 0


def bump_wrong():
    # counter += 1  # 会报 UnboundLocalError：赋值让 counter 变成了局部变量
    pass


def bump():
    global counter  # 显式声明要改全局变量；实际项目尽量别这么干
    counter += 1


bump()
print(counter)  # 1


def make_counter():
    count = 0

    def inc() -> int:
        nonlocal count  # 闭包里改外层函数变量要用 nonlocal；JS 直接改就行
        count += 1
        return count

    return inc


c = make_counter()
print(c(), c(), c())  # 1 2 3

# ====================================================
# 五、可变默认参数陷阱（Python 面试经典题）
# ====================================================


def append_bad(item, items=[]):  # noqa: B006 —— 默认值只在函数定义时创建一次！
    items.append(item)
    return items


print(append_bad(1))  # [1]
print(append_bad(2))  # [1, 2]  —— 不是 [2]！


def append_good(item, items: list | None = None):
    if items is None:
        items = []
    items.append(item)
    return items


print(append_good(1))  # [1]
print(append_good(2))  # [2]
