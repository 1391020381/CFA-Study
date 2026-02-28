# 02-数据处理库

## 目标

掌握NumPy、Pandas、Matplotlib三大核心库。

## 2.1 NumPy - 数值计算

### 基础操作

```python
import numpy as np

# 创建数组
prices = np.array([100.5, 101.2, 99.8, 102.1])
returns = np.array([0.01, 0.02, -0.01, 0.03])

# 数组运算
print(prices * 1.1)           # 所有元素乘以1.1
print(prices + 5)             # 所有元素加5
print(np.mean(prices))        # 均值
print(np.std(prices))         # 标准差
print(np.median(prices))      # 中位数

# 累积计算
np.cumsum(returns)            # 累积求和
np.cumprod(1 + returns)       # 累积乘积(计算累积收益率)
```

### 金融计算示例

```python
# 计算对数收益率
prices = np.array([100, 102, 101, 105, 103])
log_returns = np.diff(np.log(prices))

# 计算波动率(年化)
daily_returns = np.array([0.01, 0.02, -0.01, 0.005, -0.02])
volatility = np.std(daily_returns) * np.sqrt(252)

# 计算相关系数
stock1_returns = np.array([0.01, 0.02, -0.01, 0.03])
stock2_returns = np.array([0.015, 0.01, -0.005, 0.025])
correlation = np.corrcoef(stock1_returns, stock2_returns)[0, 1]
```

## 2.2 Pandas - 数据分析（核心）

### Series - 一维数据

```python
import pandas as pd

# 创建Series
prices = pd.Series([100.5, 101.2, 99.8, 102.1],
                   index=['2024-01-01', '2024-01-02',
                          '2024-01-03', '2024-01-04'])

# 基本操作
print(prices.mean())           # 均值
print(prices.std())            # 标准差
print(prices.describe())       # 描述统计

# 索引与切片
prices['2024-01-02']           # 按索引访问
prices[1:3]                    # 按位置切片
prices[prices > 100]           # 条件筛选
```

### DataFrame - 二维数据

```python
# 创建DataFrame
data = {
    'open': [100, 102, 101, 105],
    'high': [105, 106, 104, 108],
    'low': [99, 100, 99, 103],
    'close': [102, 104, 103, 106],
    'volume': [10000, 12000, 8000, 15000]
}
df = pd.DataFrame(data)

# 查看数据
df.head()                      # 前5行
df.tail()                      # 后5行
df.info()                      # 数据信息
df.describe()                  # 统计描述

# 索引操作
df['close']                    # 选择列
df[['open', 'close']]          # 选择多列
df.loc[0]                      # 按标签选择行
df.iloc[0]                     # 按位置选择行
df.loc[0, 'close']             # 选择具体值
```

### 数据处理

```python
# 时间序列
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
df.resample('M').mean()        # 按月重采样

# 数据清洗
df.dropna()                    # 删除缺失值
df.fillna(0)                   # 填充缺失值
df.drop_duplicates()           # 删除重复值

# 数据转换
df['returns'] = df['close'].pct_change()        # 收益率
df['ma5'] = df['close'].rolling(5).mean()       # 5日均线
df['cumret'] = (1 + df['returns']).cumprod()   # 累积收益

# 数据筛选
df[df['close'] > df['open']]                    # 阳线
df[(df['volume'] > 10000) & (df['returns'] > 0)]  # 多条件

# 数据分组
df.groupby(df.index.month).mean()               # 按月分组
```

### 数据合并

```python
# 合并多个股票数据
pd.concat([df1, df2, df3])

# 按日期合并
pd.merge(df_price, df_volume, on='date', how='left')
```

## 2.3 Matplotlib - 数据可视化

### 基础绘图

```python
import matplotlib.pyplot as plt

# 折线图
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['close'], label='收盘价')
plt.plot(df.index, df['ma20'], label='20日均线')
plt.title('股价走势')
plt.xlabel('日期')
plt.ylabel('价格')
plt.legend()
plt.grid(True)
plt.show()

# K线图(需要mplfinance)
import mplfinance as mpf
mpf.plot(df, type='candle', mav=(5, 10, 20), volume=True)
```

### 多子图

```python
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# 价格图
axes[0].plot(df.index, df['close'])
axes[0].set_title('价格走势')

# 成交量图
axes[1].bar(df.index, df['volume'])
axes[1].set_title('成交量')

plt.tight_layout()
plt.show()
```

### 交互式图表(Plotly)

```python
import plotly.graph_objects as go

fig = go.Figure(data=[go.Candlestick(
    x=df.index,
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close']
)])
fig.show()
```

## 综合案例：计算技术指标

```python
import pandas as pd
import numpy as np

# 假设df是包含OHLC数据的DataFrame
def add_technical_indicators(df):
    # 移动平均线
    df['MA5'] = df['close'].rolling(5).mean()
    df['MA10'] = df['close'].rolling(10).mean()
    df['MA20'] = df['close'].rolling(20).mean()

    # 收益率
    df['returns'] = df['close'].pct_change()

    # 波动率
    df['volatility'] = df['returns'].rolling(20).std()

    # RSI(简化版)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    exp1 = df['close'].ewm(span=12).mean()
    exp2 = df['close'].ewm(span=26).mean()
    df['MACD'] = exp1 - exp2
    df['Signal'] = df['MACD'].ewm(span=9).mean()

    return df

df = add_technical_indicators(df)
```

## 练习题

1. 计算股票的夏普比率
2. 实现布林带指标
3. 绘制K线图与成交量
4. 计算多只股票的相关系数矩阵

## 学习检查清单

- [ ] 理解NumPy数组与广播机制
- [ ] 熟练使用Pandas Series和DataFrame
- [ ] 掌握数据清洗与转换方法
- [ ] 能够使用Matplotlib绘制基本图表
- [ ] 理解时间序列处理方法

## 下一步

数据处理库掌握后 → [03-金融数据获取](../03-金融数据获取/)
