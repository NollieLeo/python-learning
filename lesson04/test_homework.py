"""自动检查，运行：uv run pytest lesson04"""

import json
from pathlib import Path

import pytest

from lesson04.homework import (
    ConfigError,
    InvalidAgeError,
    append_log,
    count_nonblank_lines,
    find_files,
    load_config,
    parse_age,
    safe_int,
    save_json,
)


def test_safe_int():
    assert safe_int("42") == 42
    assert safe_int(" 7 ") == 7  # int() 自己会去掉首尾空格
    assert safe_int("4.2") is None
    assert safe_int("x", default=0) == 0


def test_safe_int_only_catches_value_error():
    # 传了非字符串，int() 抛的是 TypeError，不应该被吞掉
    with pytest.raises(TypeError):
        safe_int(None)  # type: ignore[arg-type]


def test_parse_age_ok():
    assert parse_age("28") == 28
    assert parse_age("0") == 0
    assert parse_age("150") == 150


def test_parse_age_invalid():
    with pytest.raises(InvalidAgeError) as info:
        parse_age("abc")
    assert str(info.value) == "invalid age: 'abc'"
    assert info.value.value == "abc"
    assert isinstance(info.value.__cause__, ValueError)  # from e 保留了原因

    with pytest.raises(InvalidAgeError) as info:
        parse_age("200")
    assert info.value.value == "200"

    with pytest.raises(ValueError):  # InvalidAgeError 是 ValueError 的子类，接父类也能接住
        parse_age("-1")


def test_count_nonblank_lines(tmp_path: Path):
    f = tmp_path / "a.txt"
    f.write_text("one\n\n  \ntwo\nthree", encoding="utf-8")
    assert count_nonblank_lines(f) == 3
    assert count_nonblank_lines(tmp_path / "missing.txt") == 0


def test_append_log(tmp_path: Path):
    log = tmp_path / "logs" / "app.log"
    append_log(log, "hello")
    append_log(log, "world")
    assert log.read_text(encoding="utf-8") == "hello\nworld\n"


def test_load_config(tmp_path: Path):
    assert load_config(tmp_path / "missing.json") == {}

    good = tmp_path / "good.json"
    good.write_text('{"debug": true, "port": 8000}', encoding="utf-8")
    assert load_config(good) == {"debug": True, "port": 8000}

    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(ConfigError) as info:
        load_config(bad)
    assert "bad.json" in str(info.value)
    assert isinstance(info.value.__cause__, json.JSONDecodeError)


def test_save_json(tmp_path: Path):
    target = tmp_path / "out" / "cfg.json"
    data = {"name": "恺敏", "tags": ["fe", "py"], "age": None}
    save_json(target, data)
    text = target.read_text(encoding="utf-8")
    assert "恺敏" in text  # ensure_ascii=False
    assert "\n  " in text  # indent=2
    assert json.loads(text) == data


def test_find_files(tmp_path: Path):
    (tmp_path / "a.py").write_text("", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("", encoding="utf-8")
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "b.py").write_text("", encoding="utf-8")
    assert find_files(tmp_path, ".py") == ["a.py", "pkg/b.py"]
    assert find_files(tmp_path, ".md") == []
