"""Lesson 04 作业：异常与文件

规则同上：只改 TODO，不改签名，uv run pytest lesson04 全绿即完成。
文件类的题测试会传一个临时目录（tmp_path）进来，你不用自己造文件。
"""

import json  # noqa: F401 —— 作业 5、6 要用，写完之后这个 noqa 可以删
from pathlib import Path


# ---------- 作业 1：安全转整数 ----------
def safe_int(text: str, default: int | None = None) -> int | None:
    """int(text) 成功就返回结果，失败返回 default。
    safe_int("42") -> 42
    safe_int("4.2") -> None
    safe_int("x", default=0) -> 0
    要求：用 try/except，只接 ValueError，别接 Exception。
    """
    try:
        return int(text)
    except ValueError:
        return default


# ---------- 作业 2：自定义异常 ----------
class InvalidAgeError(ValueError):
    """年龄不合法。实例要有 .value 属性存原始输入，消息格式见 parse_age 的例子。"""

    def __init__(self, value: object) -> None:
        super().__init__(f"invalid age: {value!r}")
        self.value = value


def parse_age(text: str) -> int:
    """把字符串解析成 0～150 之间的整数年龄，否则抛 InvalidAgeError。
    parse_age("28") -> 28
    parse_age("abc") -> InvalidAgeError，消息 "invalid age: 'abc'"，.value == "abc"
    parse_age("200") -> InvalidAgeError，消息 "invalid age: '200'"，.value == "200"
    提示：int() 失败时用 raise ... from e 保留原因；消息里用 {text!r}。
    """
    age = 0
    try:
        age = int(text)
    except ValueError as e:
        raise InvalidAgeError(
            value=text,
        ) from e
    if not 0 <= age <= 150:
        raise InvalidAgeError(value=text)
    return age


# ---------- 作业 3：数非空行 ----------
def count_nonblank_lines(path: Path) -> int:
    """返回文件里非空行（strip 后不为空）的数量。文件不存在返回 0。
    提示：with open(path, encoding="utf-8")，逐行迭代；接 FileNotFoundError。
    """
    count = 0
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                if len(line.strip()):
                    count += 1
    except FileNotFoundError:
        return count
    return count


# ---------- 作业 4：追加日志 ----------
def append_log(path: Path, message: str) -> None:
    """把 message 作为一行追加到 path 末尾（自带换行）。父目录不存在要先建。
    连续调两次，文件里就是两行。
    提示：path.parent.mkdir(parents=True, exist_ok=True)，open 的 "a" 模式。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")


# ---------- 作业 5：读配置 ----------
class ConfigError(Exception):
    """配置文件内容不是合法 JSON。"""

    def __init__(self, path: Path) -> None:
        super().__init__(f"{path} 不是合法json")
        self.path = path


def load_config(path: Path) -> dict:
    """读 JSON 配置文件返回 dict。
    文件不存在 -> 返回 {}（这是正常情况，不是错误）
    文件存在但不是合法 JSON -> 抛 ConfigError，消息里带路径，用 from 保留原始的 JSONDecodeError
    提示：json.load；json.JSONDecodeError。
    """
    result = {}
    try:
        with open(path, encoding="utf-8") as f:
            result = json.load(f)
    except FileNotFoundError:
        return result
    except json.JSONDecodeError as e:
        raise ConfigError(path) from e
    return result


# ---------- 作业 6：写 JSON ----------
def save_json(path: Path, data: dict) -> None:
    """把 data 写成 JSON 文件：中文原样（ensure_ascii=False）、缩进 2、父目录自动创建。
    测试会检查 path.read_text() 里包含原样的中文，并且 json.loads 回来等于 data。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        text = json.dumps(data, ensure_ascii=False, indent=2)
        f.write(text)


# ---------- 作业 7：找文件 ----------
def find_files(directory: Path, suffix: str) -> list[str]:
    """递归找出 directory 下所有以 suffix 结尾的文件，返回相对 directory 的路径字符串，升序。
    find_files(tmp, ".py") -> ["a.py", "pkg/b.py"]
    提示：directory.rglob(f"*{suffix}")、p.relative_to(directory)、str()、sorted。
    """
    files = (str(p.relative_to(directory)) for p in directory.rglob(f"*{suffix}"))
    return sorted(files)


# ---------- 作业 8（思考题，写注释回答即可）----------
# 先猜输出，再运行验证：
#
# def f():
#     try:
#         return "try"
#     finally:
#         print("finally")


# print(f())

# data = {1: "a", "1": "b"}
# print(json.loads(json.dumps(data)))
#
# 你的猜测（第一段打印几行、顺序如何；第二段结果是什么）：第一段不知道。第二段也不知道
# 实际结果：finally, try。{'1': 'b'}
# 解释：
# - finally 的设计是「无论 try 怎么退出都要执行」，return 也是一种退出，所以 Python
# 先执行 finally 里的 print，再把 "try" 交出去。和 JS 行为完全一样。
# - int 的 1 经过 json.dumps 变成字符串 "1"，JSON 的 key 只能是字符串。
# 回来时两个 "1" 撞在一起，后面的 "b" 覆盖前面的 "a"，一对数据悄悄丢了。
#


QUESTIONS = """
（在这里写你学习过程中的疑问）
"""


if __name__ == "__main__":
    import tempfile

    print(safe_int("42"), safe_int("4.2"), safe_int("x", default=0))
    print(parse_age("28"))
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        append_log(root / "logs" / "app.log", "hello")
        append_log(root / "logs" / "app.log", "world")
        print(count_nonblank_lines(root / "logs" / "app.log"))
        save_json(root / "cfg.json", {"name": "恺敏"})
        print(load_config(root / "cfg.json"), load_config(root / "missing.json"))
        print(find_files(root, ".json"))
