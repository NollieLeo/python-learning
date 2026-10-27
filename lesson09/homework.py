"""Lesson 09 作业：给 inventory.py 写测试，并修好它的 3 个 bug。

这课的作业不是填函数，而是：
  1. 新建 lesson09/test_inventory.py，给 inventory.py 写测试（要求见下）
  2. 用你的测试把 inventory.py 里的 3 个 bug 找出来并修好（只改函数体）
  3. uv run pytest lesson09 全绿：既跑你的测试，也跑老师的 test_homework.py（它会检查你的测试文件
     和 bug 是否修好）

你的 test_inventory.py 至少要包含（test_homework.py 会检查）：
  - 一个 @pytest.fixture，提供预先加了几件货的 Inventory，多个测试复用它
  - 一个 @pytest.mark.parametrize，至少 3 组数据
  - pytest.raises 测 add 的 qty<=0、remove 不存在的商品、remove 超过库存
  - 用 tmp_path 测 save / load 往返，数据里要有中文商品名
  - 用 caplog 断言 remove 成功时写了 "removed" 日志
  - 用 monkeypatch 或 mock.patch 替换掉一个东西（随便哪个，比如把 Path.write_text 换成
    记录调用的假函数，或者 setattr 改掉 low_stock 的默认阈值）
  - 测 snapshot 返回的副本被修改后不影响原库存
  - 至少 10 个 test 函数（parametrize 展开后的算一个）

跑法：
  uv run pytest lesson09/test_inventory.py -v     只跑你的
  uv run pytest lesson09 -v                       全部
  uv run pytest lesson09 --cov=lesson09/inventory.py --cov-report=term-missing   看覆盖率

思考题（写注释回答）：
  1. 为什么 mock.patch 的字符串要写 "lesson09.inventory.xxx" 而不是定义 xxx 的地方？
     （提示：Lesson 05 的 from x import name 是复制名字）
  2. 一个 fixture 默认每个 test 都重新创建。如果我想整个文件只创建一次（比如很贵的数据库连接），
     怎么写？查一下 fixture 的 scope 参数。
  3. 你找到的 3 个 bug 分别是什么？各是哪条测试暴露的？
"""

# 思考题回答：
# 1. mock.patch 替换的是“某个模块命名空间里的名字”，不是对象本身。
#    inventory.py 里 `from x import xxx`（或 `log = logging.getLogger(...)`）会在 lesson09.inventory
#    这个模块的命名空间里复制一份名字 xxx；之后 inventory 里的代码查的都是自己模块里的这个名字。
#    如果 patch 定义处（比如 "logging.getLogger"），改的是 logging 模块的名字，inventory 手里那份
#    引用没变，被测代码照样调用真函数。所以要 patch “被使用处” "lesson09.inventory.xxx"。
#    类比 TS：import 进来后绑定在当前模块里，jest.mock 也要 mock 被测文件 import 的那个路径。
#
# 2. 加 scope 参数：@pytest.fixture(scope="module") 整个文件只建一次，
#    scope="session" 整个测试进程只建一次（还有 "class" / "package"，默认是 "function"）。
#    代价是测试之间会共享同一个对象，谁改了状态会影响后面的测试，所以只给「贵但只读」的资源用，
#    比如数据库连接、启动一个服务；像 Inventory 这种会被修改的数据还是 function 级每次新建。
#
# 3. 实际找到 4 处（remove 里算 2 个）：
#    - remove 没检查库存，超出也不抛，还少了 log.info("removed ...")
#        暴露：test_remove_over_stock_raises_and_keeps_state（pytest.raises + 断言 qty 没被动过），
#              test_remove_logs_removed（caplog）/
#              test_remove_calls_log_info_with_mock（mock.patch）
#    - total_value 只加 price，漏乘 qty
#        暴露：test_total_value_is_sum_of_price_times_qty（fixture 里数量故意不是 1）
#    - snapshot 直接 return self.items，不是副本
#      （Lesson 03 引用语义；浅拷贝 dict() 也不够，Item 还是同一个）
#        暴露：test_snapshot_is_a_copy（改副本后断言原库存没变）、
#              test_snapshot_content_matches（is not）
#    - save 的 write_text 没写 encoding="utf-8"
#      （Lesson 04；macOS 默认 utf-8 所以本地跑不出来，Windows 会炸）
#        暴露：test_save_passes_utf8_encoding（monkeypatch 替换 Path.write_text 记录 kwargs）

QUESTIONS = """
（在这里写你学习过程中的疑问）
"""
