"""Lesson 09 课堂示例：pytest 的常用武器。运行 uv run pytest lesson09/test_calc_demo.py -v

对照 Jest：
  def test_xxx()           ≈ test("xxx", () => {})      不需要 describe，文件/函数名就是分组
  assert a == b            ≈ expect(a).toBe(b)           只有 assert，pytest 会把两边的值打出来
  pytest.raises            ≈ expect(fn).toThrow()
  pytest.approx            ≈ toBeCloseTo
  @pytest.fixture          ≈ beforeEach + 依赖注入       按参数名注入，不是全局钩子
  @pytest.mark.parametrize ≈ test.each
  monkeypatch / mock.patch ≈ jest.spyOn / jest.mock
  tmp_path                 ≈ 自己 mkdtemp，pytest 自动清理
  capsys                   ≈ jest.spyOn(console, 'log')
  caplog                   ≈ 断言日志输出，Jest 没有直接对应
"""

import logging
from pathlib import Path
from unittest import mock

import pytest

from lesson09 import calc

# ====================================================
# 一、最基本的测试：assert 就够了
# ====================================================


def test_divide():
    assert calc.divide(10, 4) == 2.5
    # 失败时 pytest 会打印：assert 2.5 == 3，不需要 expect().toBe() 那套 matcher


def test_float_compare():
    assert calc.mean([0.1, 0.2]) == pytest.approx(0.15)  # 浮点数别用 ==


# ====================================================
# 二、断言异常：pytest.raises 是上下文管理器（Lesson 08）
# ====================================================


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError, match="must not be 0"):  # match 是正则
        calc.divide(1, 0)


def test_mean_empty_message():
    with pytest.raises(ValueError) as info:
        calc.mean([])
    assert str(info.value) == "empty"  # 需要检查异常对象时用 as info


# ====================================================
# 三、参数化：一个函数跑多组数据，≈ test.each
# ====================================================


@pytest.mark.parametrize(
    ("xs", "expected"),
    [
        ([1, 2, 3], 2),
        ([5], 5),
        ([1.5, 2.5], 2.0),
    ],
    ids=["three", "single", "floats"],  # 可选：给每组起名字，-v 时好看
)
def test_mean(xs: list[float], expected: float):
    assert calc.mean(xs) == expected


# ====================================================
# 四、fixture：按参数名注入的「准备工作」，≈ beforeEach 但更灵活
# ====================================================


@pytest.fixture
def scores_file(tmp_path: Path) -> Path:  # fixture 可以依赖别的 fixture；tmp_path 是 pytest 内置的
    p = tmp_path / "scores.json"
    p.write_text("[90, 80, 70]", encoding="utf-8")
    return p


def test_load_scores(scores_file: Path):  # 参数名 = fixture 名，pytest 自动调用并传入
    assert calc.load_scores(scores_file) == [90, 80, 70]


@pytest.fixture
def db_connection():
    print("\n  [连接]")
    conn = {"open": True}
    yield conn  # yield 前 = setup，后 = teardown（Lesson 08 的生成器 + 上下文管理器思路）
    conn["open"] = False
    print("  [断开]")


def test_uses_connection(db_connection: dict):
    assert db_connection["open"]


# 共享的 fixture 放 conftest.py，同目录及子目录的测试都能用，不用 import

# ====================================================
# 五、替换依赖：monkeypatch（pytest 内置）和 mock.patch（标准库）
# ====================================================


def test_greeting_with_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("USER_NAME", "kaimin")  # 测试结束自动还原
    assert calc.greeting() == "hello, kaimin"


def test_greeting_default(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("USER_NAME", raising=False)
    assert calc.greeting() == "hello, stranger"


def test_convert_with_monkeypatch(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(calc, "fetch_rate", lambda currency: 7.0)  # 替换模块里的函数
    assert calc.convert(10, "CNY") == 70.0


def test_convert_with_mock():
    with mock.patch(
        "lesson09.calc.fetch_rate", return_value=7.25
    ) as fake:  # 字符串路径指向「被使用处」
        assert calc.convert(10, "CNY") == 72.5
    fake.assert_called_once_with("CNY")  # mock 还能断言调用情况，≈ toHaveBeenCalledWith


# ====================================================
# 六、捕获输出和日志
# ====================================================


def test_capsys(capsys: pytest.CaptureFixture[str]):
    print("hi")
    assert capsys.readouterr().out == "hi\n"


def test_caplog(scores_file: Path, caplog: pytest.LogCaptureFixture):
    with caplog.at_level(logging.INFO):
        calc.load_scores(scores_file)
    assert "loading" in caplog.text


# ====================================================
# 七、标记：跳过、预期失败、自定义分组
# ====================================================


@pytest.mark.skip(reason="演示 skip")
def test_skipped(): ...


@pytest.mark.xfail(reason="已知 bug，修好后这个标记要删")
def test_known_bug():
    assert calc.divide(1, 3) == 0.3


@pytest.mark.slow  # 自定义标记要在 pyproject.toml 的 markers 里登记；跑 -m "not slow" 可跳过
def test_marked_slow():
    assert True
