"""Lesson 03 课堂示例：list / tuple / dict / set、切片、解包、推导式。

运行方式：uv run python lesson03/demo.py
"""

import copy

# ====================================================
# 一、list：就是 JS 的数组，但方法名不同
# ====================================================
nums = [3, 1, 2]
nums.append(4)  # push
nums.extend([5, 6])  # push(...arr)  /  concat 但是原地
nums.insert(0, 0)  # splice(0, 0, x)
last = nums.pop()  # pop()，返回被删的
first = nums.pop(0)  # shift()
nums.remove(3)  # 按值删第一个匹配，没有则 ValueError
print(nums, first, last)

print(len(nums), nums[0], nums[-1])  # 负索引从末尾数
print(nums[1:3], nums[:2], nums[::2])  # 切片：[start:stop:step]，左闭右开
print(nums.index(2), 2 in nums)  # indexOf / includes
print(nums.count(2))

nums.sort()  # 原地排序，返回 None！（和 JS sort 一样原地，但 JS 还返回自身）
print(sorted([3, 1, 2]))  # 返回新列表，原列表不变 —— 大多数时候用这个
print(sorted([3, 1, 2], reverse=True))
nums.reverse()  # 原地反转
print(list(reversed(nums)))  # 返回迭代器，list() 转成列表

print([0] * 3)  # [0, 0, 0]  —— Array(3).fill(0)
print([1, 2] + [3])  # 拼接出新列表

# ====================================================
# 二、引用语义和拷贝：和 JS 一模一样的坑
# ====================================================
a = [1, [2, 3]]
b = a  # 同一个对象
b.append(4)
print(a)  # [1, [2, 3], 4]

c = a.copy()  # 浅拷贝，等价 a[:] 或 list(a)，相当于 [...a]
c[1].append(99)
print(a)  # 内层列表还是共享的！

d = copy.deepcopy(a)  # 深拷贝，相当于 structuredClone
d[1].append(100)
print(a, d)

# ====================================================
# 三、tuple：不可变的 list，JS 没有直接对应物（最接近 readonly 元组类型）
# ====================================================
point = (3, 4)  # 括号可以省：point = 3, 4
x, y = point  # 解包，const [x, y] = point
print(x, y)
# point[0] = 10  -> TypeError，不可变
single = (1,)  # 单元素 tuple 必须带逗号，(1) 只是数字 1

a, b = 1, 2
a, b = b, a  # 交换，不需要临时变量
print(a, b)

head, *rest = [1, 2, 3, 4]  # 相当于 const [head, ...rest]
first, *_, last = [1, 2, 3, 4]  # * 可以在中间
print(head, rest, first, last)

# 什么时候用 tuple：固定结构的"记录"（坐标、RGB）、函数返回多个值、dict 的 key（list 不能做 key）
locations = {(0, 0): "origin", (1, 2): "somewhere"}
print(locations[(0, 0)])

# ====================================================
# 四、dict：JS 的对象 / Map 二合一
# ====================================================
user = {"name": "kaimin", "age": 28}  # key 必须加引号，{name: ...} 是语法错误
print(user["name"])  # 取值；key 不存在会 KeyError，不是 undefined
print(user.get("email"))  # None，相当于 user.email ?? undefined
print(user.get("email", "n/a"))  # 带默认值
user["email"] = "a@b.com"  # 新增 / 修改
del user["age"]  # delete user.age
print("name" in user)  # "name" in user —— 和 JS 一样！但 JS 的 in 查原型链，Python 只查 key
print(len(user))

for key in user:  # 默认遍历 key
    print(key)
for key, value in user.items():  # Object.entries(user)
    print(key, value)
print(list(user.keys()), list(user.values()))

user.setdefault("tags", []).append("fe")  # 没有就先设成 []，再返回它
print(user)
merged = {**user, "age": 29}  # 展开合并，和 JS 一样
merged2 = user | {"age": 30}  # 3.9+ 的合并运算符
print(merged2)
user.update({"age": 31})  # Object.assign(user, {...})

# dict 从 3.7 起保证插入顺序，和 JS 对象的行为基本一致
# key 可以是任何不可变类型：str、int、tuple，不限于字符串

# ====================================================
# 五、set：JS 的 Set，但有集合运算
# ====================================================
s = {1, 2, 2, 3}  # noqa: B033 —— {1, 2, 3} 自动去重，ruff 会提醒你字面量里有重复
print(s, len(s))
s.add(4)
s.discard(99)  # 删不存在的不报错；remove 会报错
print(2 in s)  # O(1) 成员判断，比 list 的 in 快得多
print(set([1, 1, 2]))  # 去重最常用写法：list(set(xs))
empty = set()  # 注意 {} 是空 dict，不是空 set

evens, odds = {2, 4, 6}, {1, 3, 5, 6}
print(evens & odds, evens | odds, evens - odds)  # 交、并、差，JS 要自己写

# ====================================================
# 六、推导式：map / filter 的 Python 写法
# ====================================================
nums = [1, 2, 3, 4, 5, 6]

squares = [n * n for n in nums]  # nums.map(n => n * n)
evens = [n for n in nums if n % 2 == 0]  # nums.filter(n => n % 2 === 0)
even_squares = [n * n for n in nums if n % 2 == 0]  # filter 再 map，一步到位
print(squares, evens, even_squares)

# 读法：[ 表达式 for 元素 in 可迭代 if 条件 ]，和 for 循环顺序一致
# 等价的 for 循环：
even_squares2 = []
for n in nums:
    if n % 2 == 0:
        even_squares2.append(n * n)

# dict 推导式 / set 推导式
name_len = {name: len(name) for name in ["ts", "python"]}  # Object.fromEntries(names.map(...))
unique_lens = {len(name) for name in ["ts", "go", "python"]}
print(name_len, unique_lens)

# 嵌套推导式：两层 for，从左到右读
matrix = [[1, 2], [3, 4]]
flat = [x for row in matrix for x in row]  # matrix.flat()
print(flat)

# map / filter 函数也存在，但推导式几乎总是更清晰
print(list(map(lambda n: n * 2, nums)))

# 推导式太长（超过一行、嵌套超过两层）就改回 for 循环，可读性第一

# ====================================================
# 七、几个常用内置函数
# ====================================================
print(sum(nums), min(nums), max(nums))
print(any(n > 5 for n in nums), all(n > 0 for n in nums))  # some / every
print(sorted(["banana", "kiwi", "apple"], key=len))
print(max({"a": 3, "b": 7}.items(), key=lambda kv: kv[1]))  # 找 value 最大的项
for i, (k, v) in enumerate({"a": 1, "b": 2}.items()):  # 嵌套解包
    print(i, k, v)
