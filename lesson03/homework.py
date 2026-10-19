"""Lesson 03 作业：数据结构与推导式

规则同上：只改 TODO，不改签名，uv run pytest lesson03 全绿即完成。
尽量用推导式和本课讲的方法，别用 Lesson 02 的 for + append 硬写（除非注释说明为什么）。
"""


# ---------- 作业 1：去重并排序 ----------
def unique_sorted(items: list[int]) -> list[int]:
    """去重后升序返回新列表，不修改原列表。
    unique_sorted([3, 1, 3, 2]) -> [1, 2, 3]
    提示：set + sorted，一行。
    """
    result = set(items)
    return sorted(result)


# ---------- 作业 2：词频统计 ----------
def word_count(text: str) -> dict[str, int]:
    """按空白切词，忽略大小写，统计每个词出现次数。
    word_count("a B a") -> {"a": 2, "b": 1}
    word_count("") -> {}
    提示：text.lower().split()、dict.get(key, 0) 或 setdefault。
    """
    result = {}
    for n in text.lower().split():
        result[n] = result.get(n, 0) + 1
    return result


# ---------- 作业 3：反转字典 ----------
def invert_dict(d: dict[str, int]) -> dict[int, str]:
    """key 和 value 互换。假设 value 不重复。
    invert_dict({"a": 1, "b": 2}) -> {1: "a", 2: "b"}
    要求：用 dict 推导式。
    """
    # result = {}
    # for key, val in d.items():
    #     result[val] = key
    # return result
    return {val: key for key, val in d.items()}


# ---------- 作业 4：偶数的平方 ----------
def squares_of_evens(nums: list[int]) -> list[int]:
    """只保留偶数，返回它们的平方。
    squares_of_evens([1, 2, 3, 4]) -> [4, 16]
    要求：一个 list 推导式。
    """
    result = [n**2 for n in nums if n % 2 == 0]
    return result


# ---------- 作业 5：Top N ----------
def top_n(scores: dict[str, int], n: int) -> list[tuple[str, int]]:
    """按分数从高到低取前 n 个，返回 (name, score) 的列表。分数相同的保持原插入顺序。
    top_n({"a": 1, "b": 3, "c": 2}, 2) -> [("b", 3), ("c", 2)]
    提示：sorted(scores.items(), key=..., reverse=True)，然后切片。
    """
    # 不会做，用sorted不知道怎么写
    return sorted(scores.items(), reverse=True, key=lambda x: x[1])[:n]


# ---------- 作业 6：拍平 ----------
def flatten(nested: list[list[int]]) -> list[int]:
    """二维列表拍平成一维。
    flatten([[1, 2], [], [3]]) -> [1, 2, 3]
    要求：嵌套推导式。
    """
    return [x for row in nested for x in row]


# ---------- 作业 7：分组 ----------
def group_by_length(words: list[str]) -> dict[int, list[str]]:
    """按单词长度分组，保持原顺序。
    group_by_length(["a", "bb", "c"]) -> {1: ["a", "c"], 2: ["bb"]}
    提示：setdefault(length, []).append(word)。
    """
    result = {}
    for word in words:
        length = len(word)
        result.setdefault(length, []).append(word)
    return result


# ---------- 作业 8（思考题，写注释回答即可）----------
# 先猜输出，再运行验证：
#
#   a = [1, 2, [3]]
#   b = a
#   c = a[:]
#   b.append(4)
#   c[2].append(5)
#   print(a)
#   print(c)
#
# 你的猜测：[1, 2, [3, 5], 4] [1, 2, [3, 5]]
# 实际结果：[1, 2, [3, 5], 4] [1, 2, [3, 5]]
# 解释（为什么 c[2].append(5) 会影响 a）：因为c是通过a[:]一层浅拷贝来的，但是里头下标2的元素list
# 实际上还是一个引用不受shallow clone的影响
#


QUESTIONS = """
（在这里写你学习过程中的疑问）
"""


if __name__ == "__main__":
    print(unique_sorted([3, 1, 3, 2]))
    print(word_count("a B a"))
    print(invert_dict({"a": 1, "b": 2}))
    print(squares_of_evens([1, 2, 3, 4]))
    print(top_n({"a": 1, "b": 3, "c": 2}, 2))
    print(flatten([[1, 2], [], [3]]))
    print(group_by_length(["a", "bb", "c"]))
