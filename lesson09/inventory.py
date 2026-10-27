"""作业的被测代码：一个简单的库存模块。里面埋了 3 个 bug，靠你写的测试把它们找出来并修好。

bug 的位置不告诉你。提示：边界条件、Lesson 03 的引用语义、Lesson 04 的文件编码。
修 bug 时只改函数体，不改签名。
"""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path

log = logging.getLogger(__name__)


@dataclass
class Item:
    name: str
    price: float
    qty: int = 0


@dataclass
class Inventory:
    items: dict[str, Item] = field(default_factory=dict)

    def add(self, name: str, price: float, qty: int = 1) -> None:
        """加货。已存在则累加数量并更新价格；qty <= 0 抛 ValueError("qty must be positive")。"""
        if qty <= 0:
            raise ValueError("qty must be positive")
        if name in self.items:
            self.items[name].qty += qty
            self.items[name].price = price
        else:
            self.items[name] = Item(name, price, qty)

    def remove(self, name: str, qty: int = 1) -> None:
        """出货。不存在抛 KeyError；qty 超过库存抛 ValueError("insufficient stock")；
        减到 0 时把条目删掉。每次成功出货要 log.info("removed %d x %s", qty, name)。
        """
        item = self.items[name]
        if qty > item.qty:
            raise ValueError("insufficient stock")
        item.qty -= qty
        if item.qty == 0:
            del self.items[name]
        log.info("removed %d x %s", qty, name)

    def total_value(self) -> float:
        """库存总价值 = Σ price * qty，保留 2 位小数。"""
        return round(sum(item.price * item.qty for item in self.items.values()), 2)

    def low_stock(self, threshold: int = 5) -> list[str]:
        """数量 < threshold 的商品名，按名字排序。"""
        return sorted(name for name, item in self.items.items() if item.qty < threshold)

    def snapshot(self) -> dict[str, Item]:
        """返回当前库存的副本，调用方改副本不能影响库存。"""
        return {name: Item(i.name, i.price, i.qty) for name, i in self.items.items()}

    def save(self, path: Path) -> None:
        data = {name: {"price": i.price, "qty": i.qty} for name, i in self.items.items()}
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> Inventory:
        data = json.loads(path.read_text(encoding="utf-8"))
        inv = cls()
        for name, d in data.items():
            inv.items[name] = Item(name, d["price"], d["qty"])
        return inv
