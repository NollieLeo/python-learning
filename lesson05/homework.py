"""Lesson 05 作业：模块与包。

这课的作业不在这个文件里，而是一个真正的包：
    lesson05/shapes/      -> 填 __init__.py、circle.py、rect.py、_format.py 里的 TODO
    lesson05/cli.py       -> 填 main() 和 __main__ 入口
    uv run pytest lesson05 全绿即完成。

作业 6（动手题，没有测试，批改时我看 pyproject.toml）：
    用 uv add --dev pytest-cov 装一个开发依赖，然后跑
        uv run pytest lesson05 --cov=lesson05 --cov-report=term-missing
    把输出里 lesson05/shapes/__init__.py 那一行贴到下面 QUESTIONS 里。
    观察 pyproject.toml 和 uv.lock 的变化，对照 package.json / pnpm-lock.yaml。

作业 7（思考题，写注释回答）：
    1. 在 lesson05/shapes/__init__.py 最顶上临时加一行 print("loading shapes")，
       然后跑 uv run pytest lesson05 -s，这行打印了几次？为什么不是每个 test 一次？
       （看完记得删掉那行 print）
    2. 直接运行 uv run python lesson05/shapes/circle.py 会怎样？
       改成 uv run python -m lesson05.shapes.circle 呢？解释差别。
    3. 为什么 _format.py 要以下划线开头？Python 会阻止别人 import 它吗？
"""

# 思考题回答：
# 1.
# 2.
# 3.

QUESTIONS = """
（在这里写你学习过程中的疑问，以及作业 6 的覆盖率输出）
"""
