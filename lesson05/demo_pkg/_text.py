"""下划线开头：约定为包内部使用，外面别 import。语言不阻止，只是约定（和 TS 的 @internal 类似）。"""


def shout(text: str) -> str:
    return text.upper() + "!"
