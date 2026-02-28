# 01-Python基础

## 目标

掌握Python核心语法，为量化分析打下基础。

## 学习大纲

### 1.1 基础语法

```python
# 变量与数据类型
price = 100.5           # float
shares = 1000           # int
symbol = "AAPL"         # str
is_trading = True       # bool

# 字符串操作
company = "贵州茅台"
print(f"投资标的：{company}")
```

### 1.2 数据结构

```python
# 列表 - 存储价格序列
prices = [100.5, 101.2, 99.8, 102.1]
prices.append(103.5)

# 字典 - 存储股票信息
stock = {
    "symbol": "600519",
    "name": "贵州茅台",
    "price": 1800.50,
    "pe": 35.5
}

# 集合 - 去重
symbols = {"AAPL", "MSFT", "GOOGL", "AAPL"}  # 自动去重
```

### 1.3 控制流

```python
# 条件判断
def buy_signal(price, ma20):
    if price > ma20:
        return "买入"
    elif price < ma20:
        return "卖出"
    else:
        return "持有"

# 循环
prices = [100, 102, 98, 105, 103]
for i, price in enumerate(prices):
    print(f"第{i+1}天价格: {price}")

# 列表推导式
squares = [x**2 for x in range(10)]
```

### 1.4 函数

```python
def calculate_profit(entry_price, exit_price, shares):
    """计算盈亏"""
    return (exit_price - entry_price) * shares

# 默认参数
def calculate_return(cost, current, tax_rate=0.001):
    return (current - cost) / cost

# Lambda函数
get_price = lambda stock: stock["price"]
```

### 1.5 类与对象

```python
class Stock:
    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name
        self.prices = []

    def add_price(self, price):
        self.prices.append(price)

    def get_avg_price(self):
        return sum(self.prices) / len(self.prices)

# 使用
moutai = Stock("600519", "贵州茅台")
moutai.add_price(1800)
moutai.add_price(1820)
```

### 1.6 文件操作

```python
# 读取文件
with open("data.txt", "r") as f:
    data = f.read()

# 写入文件
with open("result.txt", "w") as f:
    f.write("回测结果\n")

# JSON操作
import json
config = {"symbols": ["AAPL", "MSFT"]}
with open("config.json", "w") as f:
    json.dump(config, f)
```

### 1.7 异常处理

```python
def get_stock_price(symbol):
    try:
        # 获取股票价格
        price = fetch_price(symbol)
        return price
    except ConnectionError:
        print("网络连接失败")
    except ValueError:
        print("无效的股票代码")
    finally:
        print("查询完成")
```

### 1.8 模块与包

```python
# 导入模块
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt

# 自定义模块
# my_tools.py
def calculate_ma(prices, n=20):
    return sum(prices[-n:]) / n

# 使用
# from my_tools import calculate_ma
```

## 练习题

1. 编写函数计算简单移动平均线
2. 创建Stock类，包含买入、卖出、持仓方法
3. 读取CSV格式的股价数据
4. 实现收益率计算函数

## 学习检查清单

- [ ] 熟练使用列表、字典、集合
- [ ] 掌握函数定义与参数传递
- [ ] 理解类与对象的基本概念
- [ ] 能够进行文件读写操作
- [ ] 掌握异常处理基本语法

## 下一步

Python基础掌握后 → [02-数据处理库](../02-数据处理库/)
