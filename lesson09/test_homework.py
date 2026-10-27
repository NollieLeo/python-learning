"""老师的检查，运行：uv run pytest lesson09

两部分：(1) 检查你的 test_inventory.py 是否存在、是否用了要求的特性、能否全部通过
        (2) 直接验证 inventory.py 的 3 个 bug 是否修好
"""

import logging
import re
import subprocess
import sys
from pathlib import Path

import pytest

from lesson09.inventory import Inventory

HERE = Path(__file__).parent
STUDENT_TESTS = HERE / "test_inventory.py"


def _src() -> str:
    assert STUDENT_TESTS.exists(), "还没有 lesson09/test_inventory.py"
    return STUDENT_TESTS.read_text(encoding="utf-8")


def test_student_file_uses_required_features():
    src = _src()
    required = {
        "@pytest.fixture": r"@pytest\.fixture",
        "@pytest.mark.parametrize": r"@pytest\.mark\.parametrize",
        "pytest.raises": r"pytest\.raises",
        "tmp_path": r"\btmp_path\b",
        "caplog": r"\bcaplog\b",
        "monkeypatch 或 mock.patch": r"\bmonkeypatch\b|mock\.patch",
    }
    missing = [name for name, pat in required.items() if not re.search(pat, src)]
    assert not missing, f"test_inventory.py 缺少：{missing}"
    assert len(re.findall(r"^def test_\w+", src, flags=re.M)) >= 10, "至少 10 个 test 函数"


@pytest.mark.slow
def test_student_tests_pass():
    _src()
    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(STUDENT_TESTS), "-q", "-p", "no:cacheprovider"],
        capture_output=True,
        text=True,
        check=False,
        cwd=HERE.parent,
    )
    assert result.returncode == 0, result.stdout[-2000:] + result.stderr[-500:]
    assert " passed" in result.stdout


# ---------- 下面直接验证 3 个 bug 是否修好 ----------


def test_bug_remove_over_stock_and_missing():
    inv = Inventory()
    inv.add("apple", 1.0, 3)
    with pytest.raises(ValueError, match="insufficient stock"):
        inv.remove("apple", 5)
    assert inv.items["apple"].qty == 3  # 失败不能改状态
    with pytest.raises(KeyError):
        inv.remove("nope")


def test_remove_logs(caplog: pytest.LogCaptureFixture):
    inv = Inventory()
    inv.add("apple", 1.0, 3)
    with caplog.at_level(logging.INFO):
        inv.remove("apple", 2)
    assert "removed" in caplog.text
    assert inv.items["apple"].qty == 1
    inv.remove("apple", 1)
    assert "apple" not in inv.items


def test_bug_total_value():
    inv = Inventory()
    inv.add("apple", 1.5, 4)
    inv.add("pear", 2.0, 3)
    assert inv.total_value() == 12.0  # 1.5*4 + 2*3


def test_bug_snapshot_is_a_copy():
    inv = Inventory()
    inv.add("apple", 1.0, 3)
    snap = inv.snapshot()
    snap["apple"].qty = 999
    snap["ghost"] = snap["apple"]
    assert inv.items["apple"].qty == 3
    assert "ghost" not in inv.items


def test_bug_save_utf8(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """save 必须显式 encoding="utf-8"（Lesson 04：不写就跟系统默认走，Windows 上读中文会炸）。"""
    real_write_text = Path.write_text

    def strict_write_text(self: Path, data: str, *args: object, **kwargs: object) -> int:
        assert kwargs.get("encoding") == "utf-8", "write_text 没有显式指定 encoding='utf-8'"
        return real_write_text(self, data, *args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(Path, "write_text", strict_write_text)
    inv = Inventory()
    inv.add("苹果", 3.5, 2)
    p = tmp_path / "inv.json"
    inv.save(p)
    loaded = Inventory.load(p)
    assert loaded.items["苹果"].qty == 2
    assert loaded.items["苹果"].price == 3.5
