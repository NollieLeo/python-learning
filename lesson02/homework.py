"""Lesson 02 作业：控制流与函数

规则同上：只改 TODO，不改签名，uv run pytest lesson02 全绿即完成。
"""


# ---------- 作业 1：FizzBuzz ----------
def fizzbuzz(n: int) -> list[str]:
    """返回 1 到 n 的 FizzBuzz 列表。
    能被 3 整除 -> "Fizz"，被 5 整除 -> "Buzz"，都能 -> "FizzBuzz"，否则数字本身转成字符串。
    fizzbuzz(5) -> ["1", "2", "Fizz", "4", "Buzz"]
    提示：range(1, n + 1)、str(i)、list.append
    """
    result = []
    for num in range(1, n + 1):
        if num % 3 == 0 and num % 5 == 0:
            result.append("FizzBuzz")
        elif num % 5 == 0:
            result.append("Buzz")
        elif num % 3 == 0:
            result.append("Fizz")
        else:
            result.append(str(num))
    return result


# ---------- 作业 2：可变参数求平均 ----------
def average(*nums: float, precision: int = 2) -> float:
    """任意个数字求平均，round 到 precision 位小数；没有参数时返回 0.0。
    average(1, 2, 3) -> 2.0
    average(1, 2, precision=0) -> 2.0   （round(1.5, 0) 是 2.0，银行家舍入，别纠结）
    average() -> 0.0
    提示：len(nums)、sum(nums)
    """
    if not nums:
        return 0.0
    result = sum(nums) / len(nums)
    return round(result, precision)


# ---------- 作业 3：keyword-only 参数 ----------
def greet(name: str, greeting: str = "你好", *, punctuation: str = "！") -> str:
    """greet("kaimin") -> "你好，kaimin！"
    greet("kaimin", "早上好") -> "早上好，kaimin！"
    greet("kaimin", punctuation=".") -> "你好，kaimin."
    注意签名里的 *：punctuation 只能用关键字传，greet("a", "b", "c") 会直接报 TypeError。
    """
    return f"{greeting}，{name}{punctuation}"


# ---------- 作业 4：找第一个负数 ----------
def first_negative(nums: list[int]) -> int | None:
    """返回列表里第一个负数；没有则返回 None。
    first_negative([3, -1, -5]) -> -1
    first_negative([1, 2]) -> None
    要求：用 for 循环 + return 提前返回（或者试试 for...else）。
    """
    for n in nums:
        if n < 0:
            return n
    return None


# ---------- 作业 5：高阶函数 ----------
def apply_n_times(fn, x, n: int):
    """把 fn 连续作用在 x 上 n 次。
    apply_n_times(lambda v: v * 2, 1, 3) -> 8
    apply_n_times(str.upper, "a", 1) -> "A"
    apply_n_times(lambda v: v + 1, 0, 0) -> 0
    """
    result = x
    for _i in range(n):
        result = fn(result)
    return result


# ---------- 作业 6（思考题，写注释回答即可）----------
# 先不运行，猜一下下面代码会打印什么，然后再运行 demo.py 的第五节验证：
#
#   def add_item(item, items=[]):
#       items.append(item)
#       return items
#   print(add_item("a"))
#   print(add_item("b"))
#
# 你的猜测：["a"] ["a", "b"]
# 实际结果：["a"] ["a", "b"]
# 为什么（用一句话解释）：因为items=[]相当于是在函数add_item上声明了个局部list，每次调用add_item，
# append并且返回的都是同一个list
#


QUESTIONS = """
（在这里写你学习过程中的疑问）
"""


if __name__ == "__main__":
    print(fizzbuzz(15))
    print(average(1, 2, 3))
    print(greet("kaimin", punctuation="."))
    print(first_negative([3, -1, -5]))
    print(apply_n_times(lambda v: v * 2, 1, 3))
