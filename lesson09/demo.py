"""Lesson 09 课堂示例（第二部分）：logging 与调试。

运行方式：uv run python -m lesson09.demo
测试示例在 test_calc_demo.py：uv run pytest lesson09/test_calc_demo.py -v
"""

import logging

# ====================================================
# 一、logging：别再 print 了
# ====================================================
# 每个模块顶部：
log = logging.getLogger(__name__)  # 名字自动是 "lesson09.demo"，日志里能看到来源

# 入口处配置一次（库代码绝不配置，只拿 logger 用）：
logging.basicConfig(
    level=logging.INFO,  # DEBUG < INFO < WARNING < ERROR < CRITICAL；低于 level 的不输出
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

log.debug("调试细节，默认不显示")  # 因为 level 是 INFO
log.info("程序正常运行的里程碑")
log.warning("不正常但还能继续")
log.error("出错了")

user_id, count = 42, 3
log.info("user %s has %d items", user_id, count)  # 用 % 占位，不要 f-string：
# 1) 日志级别不够时根本不会格式化，省性能  2) 日志系统能按模板聚合

try:
    _ = 1 / 0
except ZeroDivisionError:
    log.exception("计算失败")  # 在 except 里用 exception()，自动附带堆栈

# 对照 Node：≈ pino / winston 的 logger.info()；print ≈ console.log，只适合一次性脚本

# ====================================================
# 二、调试：breakpoint()
# ====================================================


def buggy(xs: list[int]) -> int:
    total = 0
    for x in xs:
        # breakpoint()  # 取消注释，运行时会停在这里进入 pdb（≈ debugger 语句）
        total += x
    return total


print(buggy([1, 2, 3]))

# pdb 常用命令（和 Chrome DevTools 对照）：
#   n  next，单步跳过          s  step，进入函数
#   c  continue                 p 变量名  打印（print）
#   pp 变量名  漂亮打印         l  list，看当前代码
#   w  where，看调用栈          q  quit
# pytest 里：uv run pytest --pdb 在第一个失败处自动进入 pdb；-x 第一个失败就停；-l 打印局部变量
# VS Code：装了 Python 扩展后直接点行号打断点、F5 运行，和调 Node 一样。
# 测试面板里每个 test 旁边有 debug 按钮，这是最常用的调试方式。

# ====================================================
# 三、几条 pytest 命令
# ====================================================
# uv run pytest                        全部
# uv run pytest lesson09 -v            详细输出，看每个用例名
# uv run pytest -k "mean and not empty" 按名字过滤
# uv run pytest -x                     第一个失败就停
# uv run pytest --lf                   只跑上次失败的（last failed）
# uv run pytest -s                     不捕获 print，让输出直接显示
# uv run pytest -m "not slow"          按标记过滤
# uv run pytest --cov=lesson09         覆盖率（Lesson 05 装过 pytest-cov）
