"""自动检查，运行：uv run pytest lesson01"""

from lesson01.homework import celsius_to_fahrenheit, introduce, is_palindrome


def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit(0) == 32.0
    assert celsius_to_fahrenheit(100) == 212.0
    assert celsius_to_fahrenheit(36.6) == 97.9


def test_introduce():
    assert introduce("kaimin", 28, ["ts", "node"]) == "我是 kaimin，28 岁，会 ts、node"
    assert introduce("小明", 20, ["python"]) == "我是 小明，20 岁，会 python"


def test_is_palindrome():
    assert is_palindrome("Level") is True
    assert is_palindrome(" abc ") is False
    assert is_palindrome("上海自来水来自海上") is True
    assert is_palindrome("") is True
    # 批改后补充的用例：首尾空格要先去掉再比较
    assert is_palindrome(" aba") is True
    assert is_palindrome("Aba ") is True
