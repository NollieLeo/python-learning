"""Lesson 09 作业：给 inventory.py 写测试。运行 uv run pytest lesson09/test_inventory.py -v

思路（对照 Jest）：
  fixture        ≈ beforeEach + 依赖注入，按参数名注入，一份预置库存多个测试复用
  parametrize    ≈ test.each，一个函数跑多组数据
  pytest.raises  ≈ expect(fn).toThrow()
  tmp_path       ≈ 自己 mkdtemp，pytest 自动清理
  caplog         ≈ 断言日志输出
  monkeypatch    ≈ jest.spyOn，测试结束自动还原
  mock.patch     ≈ jest.mock，还能断言调用情况
"""

import logging
from pathlib import Path
from unittest import mock

import pytest

from lesson09.inventory import Inventory, Item


@pytest.fixture
def stocked() -> Inventory:
    """三件货：apple 10 个、pear 3 个、苹果 2 个。每个测试拿到的都是全新的一份。"""
    inv = Inventory()
    inv.add("apple", 1.5, 10)
    inv.add("pear", 2.0, 3)
    inv.add("苹果", 3.5, 2)
    return inv


def test_add_new_item():
    inv = Inventory()
    inv.add("apple", 1.5, 4)
    assert inv.items["apple"] == Item("apple", 1.5, 4)


def test_add_default_qty_is_one():
    inv = Inventory()
    inv.add("apple", 1.5)
    assert inv.items["apple"].qty == 1


def test_add_existing_accumulates_qty_and_updates_price(stocked: Inventory):
    stocked.add("apple", 2.0, 5)
    assert stocked.items["apple"].qty == 15
    assert stocked.items["apple"].price == 2.0


@pytest.mark.parametrize("bad_qty", [0, -1, -100], ids=["zero", "negative", "very-negative"])
def test_add_rejects_non_positive_qty(stocked: Inventory, bad_qty: int):
    with pytest.raises(ValueError, match="qty must be positive"):
        stocked.add("apple", 1.5, bad_qty)
    assert stocked.items["apple"].qty == 10


def test_remove_decrements_qty(stocked: Inventory):
    stocked.remove("apple", 4)
    assert stocked.items["apple"].qty == 6


def test_remove_to_zero_deletes_entry(stocked: Inventory):
    stocked.remove("pear", 3)
    assert "pear" not in stocked.items


def test_remove_missing_item_raises_key_error(stocked: Inventory):
    with pytest.raises(KeyError):
        stocked.remove("banana")


def test_remove_over_stock_raises_and_keeps_state(stocked: Inventory):
    with pytest.raises(ValueError, match="insufficient stock"):
        stocked.remove("pear", 4)
    assert stocked.items["pear"].qty == 3


def test_remove_logs_removed(stocked: Inventory, caplog: pytest.LogCaptureFixture):
    with caplog.at_level(logging.INFO, logger="lesson09.inventory"):
        stocked.remove("apple", 2)
    assert "removed 2 x apple" in caplog.text


def test_remove_failure_does_not_log(stocked: Inventory, caplog: pytest.LogCaptureFixture):
    with caplog.at_level(logging.INFO, logger="lesson09.inventory"):
        with pytest.raises(ValueError):
            stocked.remove("pear", 99)
    assert "removed" not in caplog.text


def test_remove_calls_log_info_with_mock(stocked: Inventory):
    with mock.patch("lesson09.inventory.log") as fake_log:
        stocked.remove("apple", 3)
    fake_log.info.assert_called_once_with("removed %d x %s", 3, "apple")


def test_total_value_is_sum_of_price_times_qty(stocked: Inventory):
    assert stocked.total_value() == pytest.approx(28.0)


def test_total_value_empty_is_zero():
    assert Inventory().total_value() == 0


def test_total_value_rounds_to_two_decimals():
    inv = Inventory()
    inv.add("gum", 0.333, 3)
    assert inv.total_value() == 1.0


@pytest.mark.parametrize(
    ("threshold", "expected"),
    [
        (1, []),
        (3, ["苹果"]),
        (5, ["pear", "苹果"]),
        (100, ["apple", "pear", "苹果"]),
    ],
    ids=["none", "only-one", "two-sorted", "all"],
)
def test_low_stock(stocked: Inventory, threshold: int, expected: list[str]):
    assert stocked.low_stock(threshold) == expected


def test_low_stock_default_threshold_is_five(stocked: Inventory):
    assert stocked.low_stock() == ["pear", "苹果"]


def test_snapshot_is_a_copy(stocked: Inventory):
    snap = stocked.snapshot()
    snap["apple"].qty = 999
    snap["ghost"] = Item("ghost", 0.0, 1)
    del snap["pear"]
    assert stocked.items["apple"].qty == 10
    assert "ghost" not in stocked.items
    assert "pear" in stocked.items


def test_snapshot_content_matches(stocked: Inventory):
    snap = stocked.snapshot()
    assert snap == stocked.items
    assert snap is not stocked.items


def test_save_load_roundtrip(stocked: Inventory, tmp_path: Path):
    p = tmp_path / "inv.json"
    stocked.save(p)
    loaded = Inventory.load(p)
    assert loaded == stocked
    assert loaded.items["苹果"] == Item("苹果", 3.5, 2)


def test_save_writes_readable_chinese(stocked: Inventory, tmp_path: Path):
    p = tmp_path / "inv.json"
    stocked.save(p)
    text = p.read_text(encoding="utf-8")
    assert "苹果" in text


def test_save_passes_utf8_encoding(
    stocked: Inventory, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    """Lesson 04：write_text 不写 encoding 就跟系统默认走，Windows 上读中文会炸。"""
    calls: list[dict] = []
    real_write_text = Path.write_text

    def recording_write_text(self: Path, data: str, *args, **kwargs) -> int:
        calls.append(kwargs)
        return real_write_text(self, data, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", recording_write_text)
    stocked.save(tmp_path / "inv.json")
    assert len(calls) == 1
    assert calls[0].get("encoding") == "utf-8"


def test_load_empty_file_gives_empty_inventory(tmp_path: Path):
    p = tmp_path / "empty.json"
    p.write_text("{}", encoding="utf-8")
    assert Inventory.load(p).items == {}
