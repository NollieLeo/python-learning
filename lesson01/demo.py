"""Lesson 01 课堂示例：跟着飞书文档一段一段运行。

运行方式：uv run python lesson01/demo.py
"""

# ---------- 1. 变量：没有 let/const，没有分号 ----------
name = "kaimin"  # str
age = 28  # int
height = 1.75  # float
is_fe = True  # bool（注意大写 T）
nothing = None  # 相当于 null / undefined 二合一
fuck = float("20.1")

print(type(fuck), type(name), type(age), type(height), type(is_fe), type(nothing))

# ---------- 2. f-string：相当于模板字符串 ----------
print(f"我是 {name}，今年 {age} 岁，明年 {age + 1} 岁")
print(f"{height:.1f} 米")  # 格式化：保留 1 位小数

# ---------- 3. 数字：// 整除、** 幂、大整数不溢出 ----------
print(7 / 2)  # 3.5   —— 和 JS 一样
print(7 // 2)  # 3     —— 整除，JS 要 Math.floor
print(7 % 2)  # 1
print(2**10)  # 1024  —— JS 也有 **
print(2**100)  # 一个 31 位的大整数，不会变成 Infinity / 精度丢失

# ---------- 4. 字符串常用操作 ----------
s = "  Hello, Python  "
print(s.strip())  # trim
print(s.strip().lower())  # toLowerCase
print(s.strip().split(","))  # split
print("-".join(["a", "b", "c"]))  # ["a","b","c"].join("-")  —— 注意顺序反过来！
print(len(s))  # 没有 .length，用 len()
print("Py" in s)  # includes
print(s[2:7])  # slice(2, 7)
print(s[-3:])  # slice(-3)

# ---------- 5. 真值判断：空的就是假 ----------
for value in [0, "", [], {}, None, "0", [0]]:
    print(repr(value), "->", bool(value))
# 注意："0" 在 JS 是 true，在 Python 也是 True；但 [] 和 {} 在 JS 是 true，在 Python 是 False！

# ---------- 6. 比较：== 比值，is 比身份 ----------
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)  # True  —— 比内容（JS 里 [1,2,3] === [1,2,3] 是 false）
print(a is b)  # False —— 不是同一个对象
print(nothing is None)  # 判断 None 用 is，不用 ==

# ---------- 7. 逻辑运算：and / or / not，而不是 && || ! ----------
print(age > 18 and is_fe)
print(not is_fe)
print(None or "默认值")  # 和 JS 的 || 一样会短路返回

# ---------- 8. 输入输出 ----------
# input() 相当于一个同步的 readline，返回的永远是 str
# user = input("你叫什么名字？")
# print(f"你好，{user}")
