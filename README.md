# Python Learning

前端工程师（TS / Node / NestJS）转 Python 的学习仓库。

- 远程仓库：https://github.com/NollieLeo/python-learning
- 学习计划与进度：https://functorz.feishu.cn/wiki/Bnf6wjyTAihiYfkV2WZcMwpWnXg
- 问答记录：https://functorz.feishu.cn/wiki/QzWPwnu4qiqiGdkQgxgc8hKinOd
- 每课一个目录：`lessonXX/`，内含 `demo.py`（课堂示例）、`homework.py`（作业）、`test_homework.py`（自动检查）

## 常用命令

```bash
uv run python lesson01/demo.py      # 运行示例
uv run python lesson01/homework.py  # 运行作业
uv run pytest lesson01              # 跑某一课作业的自动检查
uv run pytest                       # 跑全部
uv run ruff format . && uv run ruff check .   # 格式化 + lint
uv run python -m lesson05.demo      # 包里的文件用 -m 跑（Lesson 05 起）
uv run python                        # 进入 REPL（相当于 node）
```
