"""Lesson 04 课堂示例：异常、with、文件读写、pathlib、json。

运行方式：uv run python lesson04/demo.py
文件操作都在一个临时目录里做，跑完自动删掉，不会在仓库里留垃圾。
"""

import json
import tempfile
from pathlib import Path

# ====================================================
# 一、try / except / else / finally：就是 try / catch / finally
# ====================================================
try:
    n = int("42")  # 可能抛 ValueError
except ValueError as e:  # catch (e)，但只接 ValueError 这一类
    print("不是数字：", e)
else:  # try 里没抛异常才执行（JS 没有这一段）
    print("解析成功：", n)
finally:  # 不管抛不抛都执行
    print("收尾")

# 异常是类，按类型接。可以接多个，也可以一次接一组
try:
    {}["missing"]
except (KeyError, IndexError) as e:
    print(type(e).__name__, e)  # KeyError 'missing'

# except Exception 接住几乎所有「程序错误」。裸 except: 连 Ctrl+C 都接，别写
try:
    _ = 1 / 0
except Exception as e:
    print("兜底：", repr(e))


# raise 就是 throw；raise ... from e 保留原因链，排错时能看到两层堆栈
def parse_port(text: str) -> int:
    try:
        port = int(text)
    except ValueError as e:
        raise ValueError(f"端口必须是整数，收到 {text!r}") from e
    if not 0 < port < 65536:
        raise ValueError(f"端口超出范围：{port}")
    return port


try:
    parse_port("abc")
except ValueError as e:
    print(e, "| 原因：", repr(e.__cause__))

# ====================================================
# 二、EAFP：先做再说，出错再接。和 JS 里「先判断再做」的习惯相反
# ====================================================
config = {"host": "localhost"}

# LBYL（Look Before You Leap）：JS 风格
port = config["port"] if "port" in config else 8000
# EAFP（Easier to Ask Forgiveness than Permission）：Python 风格
try:
    port = config["port"]
except KeyError:
    port = 8000
# 这个例子用 dict.get 最短；但「操作本身可能失败」的场景（打开文件、转换类型）EAFP 更干净
port = config.get("port", 8000)
print(port)

# 常见内置异常，接的时候要用对类型：
#   ValueError   值不对（int("x")）        TypeError    类型不对（1 + "x"）
#   KeyError     dict 没这个 key            IndexError   list 越界
#   FileNotFoundError 文件不存在           ZeroDivisionError
#   都继承自 Exception；Exception 又继承自 BaseException（KeyboardInterrupt 在那一层）


# ====================================================
# 三、自定义异常：继承 Exception 的普通类，和 class MyError extends Error 一样
# ====================================================
class ConfigError(Exception):
    """配置文件有问题。带上路径，方便上层报错时定位。"""

    def __init__(self, path: Path, reason: str) -> None:
        super().__init__(f"{path}: {reason}")
        self.path = path
        self.reason = reason


class ConfigMissingError(ConfigError):
    pass


try:
    raise ConfigMissingError(Path("app.json"), "文件不存在")
except ConfigError as e:  # 接父类就能接住所有子类
    print(type(e).__name__, "|", e, "|", e.path)

# 约定：异常类名以 Error 结尾；按「调用方会怎么处理」分层级，不要每种小错都建一个类

# ====================================================
# 四、with：上下文管理器，自动调用清理逻辑。相当于 try/finally 的语法糖
# ====================================================
# 没有 with 的写法：
# f = open(p)
# try:
#     data = f.read()
# finally:
#     f.close()
#
# 有 with：离开代码块（正常结束、return、抛异常）都会自动 close
# JS 里要到 TC39 的 using 声明（显式资源管理提案，TS 5.2+ 支持）才有对应物

with tempfile.TemporaryDirectory() as tmp:  # 临时目录，退出 with 时整个删掉
    root = Path(tmp)

    # ====================================================
    # 五、文件读写：open(path, mode, encoding)
    # ====================================================
    note = root / "note.txt"  # Path 用 / 拼路径，不用 path.join

    with open(note, "w", encoding="utf-8") as f:  # "w" 覆盖写，没有会创建
        f.write("第一行\n")
        f.write("第二行\n")
    with open(note, "a", encoding="utf-8") as f:  # "a" 追加
        f.write("第三行\n")

    with open(note, encoding="utf-8") as f:  # 默认 "r"
        content = f.read()  # 整个读成一个字符串
    print(repr(content))

    with open(note, encoding="utf-8") as f:
        for line in f:  # 逐行迭代，大文件也不会把内存撑爆；每行末尾带 \n
            print(line.rstrip("\n"))

    # encoding 永远显式写 utf-8。不写的话跟系统默认走，Windows 上会是 gbk，读中文直接炸

    # ====================================================
    # 六、pathlib：面向对象的路径，替代 os.path 那堆函数
    # ====================================================
    print(note.name, note.stem, note.suffix, note.parent.name)  # note.txt note .txt <tmp>
    print(note.exists(), note.is_file(), root.is_dir())

    # 小文件直接 read_text / write_text，连 open 都省了
    (root / "hello.txt").write_text("hi", encoding="utf-8")
    print((root / "hello.txt").read_text(encoding="utf-8"))

    sub = root / "logs" / "2026"
    sub.mkdir(parents=True, exist_ok=True)  # mkdir -p；不加 exist_ok 第二次会 FileExistsError
    (sub / "a.log").write_text("", encoding="utf-8")
    (sub / "b.log").write_text("", encoding="utf-8")
    print(sorted(p.name for p in sub.glob("*.log")))  # 当前目录通配
    print(sorted(p.name for p in root.rglob("*.log")))  # 递归

    print(Path.cwd().name, Path.home().name)  # process.cwd() / os.homedir()
    print(Path(__file__).resolve().parent.name)  # 当前脚本所在目录，相当于 __dirname

    # ====================================================
    # 七、json：JSON.stringify / JSON.parse
    # ====================================================
    user = {"name": "恺敏", "tags": ["fe", "py"], "age": None, "pos": (1, 2)}

    text = json.dumps(user)  # JSON.stringify(user)
    print(text)  # 中文默认转成 \uXXXX，None 变 null，tuple 变数组

    text = json.dumps(user, ensure_ascii=False, indent=2)  # 中文原样输出 + 缩进
    print(text)

    back = json.loads(text)  # JSON.parse
    print(back["pos"], type(back["pos"]).__name__)  # 回来是 list，tuple 信息丢了

    # dump / load 直接对文件，不用自己 read / write
    cfg = root / "config.json"
    with open(cfg, "w", encoding="utf-8") as f:
        json.dump(user, f, ensure_ascii=False, indent=2)
    with open(cfg, encoding="utf-8") as f:
        print(json.load(f)["name"])

    # 坏 JSON 抛 json.JSONDecodeError，它是 ValueError 的子类
    try:
        json.loads("{bad json}")
    except json.JSONDecodeError as e:
        print("JSON 错误：", e.msg, "第", e.lineno, "行")

    # 类型映射：dict↔object  list/tuple→array  str↔string  int/float↔number
    #          True/False↔true/false  None↔null
    # dict 的非字符串 key 会被转成字符串：json.loads(json.dumps({1: "a"})) == {"1": "a"}
    print(json.loads(json.dumps({1: "a"})))
    # 其他类型（Path、datetime、set）dumps 直接 TypeError，要先转成基本类型或传 default=str
    print(json.dumps({"p": Path("a/b")}, default=str))

print("临时目录已清理：", not Path(tmp).exists())
