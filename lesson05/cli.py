"""作业：一个最小命令行工具。

运行方式：uv run python -m lesson05.cli circle 2
          uv run python -m lesson05.cli rect 2 3

要求：
1. 用绝对导入 from lesson05.shapes import describe（脚本层用绝对导入）。
2. main(argv) 解析参数并 print 结果，成功返回 0；参数不对 print 用法并返回 2。
3. 底部用 if __name__ == "__main__" 把 sys.argv[1:] 交给 main，并用返回值作为退出码。
"""

import sys  # noqa: F401 —— __main__ 入口要用 sys.argv，写完入口后把这个 noqa 删掉

from lesson05.shapes import describe

USAGE = "usage: python -m lesson05.cli circle <r> | rect <w> <h>"


def main(argv: list[str]) -> int:
    """main(["circle", "2"]) 打印 describe("circle", r=2.0) 的结果，返回 0
    main(["rect", "2", "3"]) 打印 describe("rect", w=2.0, h=3.0) 的结果，返回 0
    main([]) / main(["triangle", "1"]) / main(["circle"]) 打印 USAGE，返回 2
    提示：float(x) 转数字；参数个数不对也算用法错误。
    """
    if not argv:
        print(USAGE)
        return 2
    kind, *values = argv
    value_l = len(values)
    if kind == "circle" and value_l == 1:
        print(describe(kind=kind, r=float(values[0])))
        return 0
    elif kind == "rect" and value_l == 2:
        print(describe(kind=kind, w=float(values[0]), h=float(values[1])))
        return 0
    else:
        print(USAGE)
        return 2


# TODO: __main__ 入口
if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
