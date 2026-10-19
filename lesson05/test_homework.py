"""自动检查，运行：uv run pytest lesson05"""

import math

import pytest

from lesson05 import shapes
from lesson05.cli import USAGE, main
from lesson05.shapes import _format, circle, rect


def test_circle():
    assert circle.area(1) == pytest.approx(math.pi)
    assert circle.perimeter(1) == pytest.approx(2 * math.pi)


def test_rect():
    assert rect.area(2, 3) == 6
    assert rect.perimeter(2, 3) == 10


def test_fmt():
    assert _format.fmt(3.14159) == "3.14"
    assert _format.fmt(6) == "6.00"


def test_package_reexports():
    # 包这一层能直接拿到 4 个函数，调用方不需要知道内部文件
    assert shapes.circle_area(1) == pytest.approx(math.pi)
    assert shapes.rect_perimeter(2, 3) == 10
    assert set(shapes.__all__) == {
        "circle_area",
        "circle_perimeter",
        "rect_area",
        "rect_perimeter",
        "describe",
    }
    assert "fmt" not in shapes.__all__


def test_describe():
    assert shapes.describe("circle", r=1) == "circle: area=3.14, perimeter=6.28"
    assert shapes.describe("rect", w=2, h=3) == "rect: area=6.00, perimeter=10.00"
    with pytest.raises(ValueError, match="unknown shape: 'hexagon'"):
        shapes.describe("hexagon", n=6)


def test_cli_ok(capsys):
    assert main(["circle", "2"]) == 0
    assert capsys.readouterr().out.strip() == "circle: area=12.57, perimeter=12.57"
    assert main(["rect", "2", "3"]) == 0
    assert capsys.readouterr().out.strip() == "rect: area=6.00, perimeter=10.00"


@pytest.mark.parametrize("argv", [[], ["triangle", "1"], ["circle"], ["rect", "1"]])
def test_cli_usage(capsys, argv):
    assert main(argv) == 2
    assert USAGE in capsys.readouterr().out


def test_cli_has_main_guard():
    # 文件末尾必须有 __main__ 入口；读源码检查，顺便练 pathlib
    from pathlib import Path

    src = (Path(__file__).parent / "cli.py").read_text(encoding="utf-8")
    assert 'if __name__ == "__main__":' in src
