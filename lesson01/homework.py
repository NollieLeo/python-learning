"""Lesson 01 作业

规则：
1. 只修改标记为 TODO 的地方，不要改函数签名。
2. 写完后运行 uv run pytest lesson01 查看是否全部通过。
3. 遇到卡住的地方，把问题写在文件末尾的 QUESTIONS 里，我来批改时会回答。
"""


# ---------- 作业 1：温度换算 ----------
def celsius_to_fahrenheit(c: float) -> float:
    """摄氏转华氏：F = C * 9 / 5 + 32，结果保留 1 位小数（用 round）。"""
    fahrenheit = c * 9 / 5 + 32
    return round(fahrenheit, 1)


# ---------- 作业 2：自我介绍 ----------
def introduce(name: str, age: int, skills: list[str]) -> str:
    """返回一句话，例如：
    introduce("kaimin", 28, ["ts", "node"]) -> "我是 kaimin，28 岁，会 ts、node"
    要求：用 f-string 和 "、".join(...)
    """
    return f"我是 {name}，{age} 岁，会 {'、'.join(skills)}"


# ---------- 作业 3：判断是否为回文 ----------
def is_palindrome(text: str) -> bool:
    """忽略大小写和首尾空格，判断是否回文。
    is_palindrome("Level") -> True
    is_palindrome(" abc ") -> False
    提示：字符串切片 [::-1] 可以反转。
    """
    lower_text = text.lower().strip()
    reversed_lower_text = lower_text[::-1]
    return lower_text == reversed_lower_text


# ---------- 作业 4（思考题，写注释回答即可）----------
# 下面这几个值在 Python 里 bool() 的结果是什么？先猜，再运行 demo.py 验证，把你猜错的写在这里：
#   0, "0", "", [], [0], {}, None
# 你的回答：
# False True False False True False False


QUESTIONS = """
（在这里写你学习过程中的疑问）
1. 这个raise NotImplementedError是干啥用的？
"""


if __name__ == "__main__":
    # 这里相当于 Node 的 if (require.main === module)，只在直接运行时执行
    print(celsius_to_fahrenheit(100))
    print(introduce("kaimin", 28, ["ts", "node", "nestjs"]))
    print(is_palindrome("Level"))
