# 04-技术指标计算

## 目标

掌握常用技术指标的原理与Python实现。

## 4.1 趋势类指标

### 移动平均线(MA)

```python
def calculate_ma(df, periods=[5, 10, 20, 60]):
    """计算简单移动平均线"""
    for period in periods:
        df[f'MA{period}'] = df['close'].rolling(window=period).mean()
    return df

# 指数移动平均
def calculate_ema(df, periods=[12, 26]):
    """计算指数移动平均"""
    for period in periods:
        df[f'EMA{period}'] = df['close'].ewm(span=period, adjust=False).mean()
    return df
```

### MACD

```python
def calculate_macd(df, fast=12, slow=26, signal=9):
    """计算MACD指标"""
    # 计算快速和慢速EMA
    ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow, adjust=False).mean()

    # DIF线
    df['MACD_DIF'] = ema_fast - ema_slow

    # DEA线(信号线)
    df['MACD_DEA'] = df['MACD_DIF'].ewm(span=signal, adjust=False).mean()

    # MACD柱
    df['MACD_Hist'] = (df['MACD_DIF'] - df['MACD_DEA']) * 2

    return df
```

### 布林带(BOLL)

```python
def calculate_bollinger(df, period=20, std_dev=2):
    """计算布林带"""
    df['BOLL_MID'] = df['close'].rolling(period).mean()
    std = df['close'].rolling(period).std()

    df['BOLL_UP'] = df['BOLL_MID'] + std_dev * std
    df['BOLL_LOW'] = df['BOLL_MID'] - std_dev * std

    # 带宽(衡量波动率)
    df['BOLL_WIDTH'] = (df['BOLL_UP'] - df['BOLL_LOW']) / df['BOLL_MID']

    return df
```

## 4.2 震荡类指标

### RSI(相对强弱指标)

```python
def calculate_rsi(df, period=14):
    """计算RSI指标"""
    # 计算价格变化
    delta = df['close'].diff()

    # 分离上涨和下跌
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # 计算平均涨跌幅
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    # 计算RSI
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    return df
```

### KDJ指标

```python
def calculate_kdj(df, n=9, m1=3, m2=3):
    """计算KDJ指标"""
    low_list = df['low'].rolling(window=n).min()
    high_list = df['high'].rolling(window=n).max()

    # RSV值
    rsv = (df['close'] - low_list) / (high_list - low_list) * 100

    # K、D、J值
    df['K'] = rsv.ewm(com=m1-1, adjust=False).mean()
    df['D'] = df['K'].ewm(com=m2-1, adjust=False).mean()
    df['J'] = 3 * df['K'] - 2 * df['D']

    return df
```

### 威廉指标(WR)

```python
def calculate_williams_r(df, period=14):
    """计算威廉指标"""
    high_high = df['high'].rolling(period).max()
    low_low = df['low'].rolling(period).min()

    df['WR'] = (high_high - df['close']) / (high_high - low_low) * -100

    return df
```

## 4.3 成交量指标

### 成交量移动平均

```python
def calculate_volume_ma(df, periods=[5, 10, 20]):
    """计算成交量均线"""
    for period in periods:
        df[f'VMA{period}'] = df['volume'].rolling(period).mean()
    return df
```

### OBV(能量潮)

```python
def calculate_obv(df):
    """计算OBV能量潮"""
    obv = [0]
    for i in range(1, len(df)):
        if df['close'].iloc[i] > df['close'].iloc[i-1]:
            obv.append(obv[-1] + df['volume'].iloc[i])
        elif df['close'].iloc[i] < df['close'].iloc[i-1]:
            obv.append(obv[-1] - df['volume'].iloc[i])
        else:
            obv.append(obv[-1])

    df['OBV'] = obv
    return df
```

### 量比

```python
def calculate_volume_ratio(df, period=5):
    """计算量比"""
    # 当日成交量 / 过去5日平均成交量
    avg_volume = df['volume'].rolling(period).mean()
    df['Volume_Ratio'] = df['volume'] / avg_volume

    return df
```

## 4.4 技术信号生成

```python
def generate_signals(df):
    """生成交易信号"""

    # 初始化信号
    df['signal'] = 0  # 0:观望, 1:买入, -1:卖出

    # 金叉死叉
    ma_cross = (df['MA5'] > df['MA20']) & (df['MA5'].shift(1) <= df['MA20'].shift(1))
    df.loc[ma_cross, 'signal'] = 1

    ma_death = (df['MA5'] < df['MA20']) & (df['MA5'].shift(1) >= df['MA20'].shift(1))
    df.loc[ma_death, 'signal'] = -1

    # MACD金叉
    macd_gold = (df['MACD_DIF'] > df['MACD_DEA']) & (df['MACD_DIF'].shift(1) <= df['MACD_DEA'].shift(1))
    df.loc[macd_gold, 'signal'] = 1

    # MACD死叉
    macd_death = (df['MACD_DIF'] < df['MACD_DEA']) & (df['MACD_DIF'].shift(1) >= df['MACD_DEA'].shift(1))
    df.loc[macd_death, 'signal'] = -1

    # RSI超卖
    rsi_oversold = (df['RSI'] < 20) & (df['RSI'].shift(1) >= 20)
    df.loc[rsi_oversold, 'signal'] = 1

    # RSI超买
    rsi_overbought = (df['RSI'] > 80) & (df['RSI'].shift(1) <= 80)
    df.loc[rsi_overbought, 'signal'] = -1

    return df
```

## 4.5 综合技术分析

```python
def comprehensive_technical_analysis(df):
    """综合技术分析"""

    # 1. 趋势类指标
    df = calculate_ma(df, [5, 10, 20, 60])
    df = calculate_macd(df)
    df = calculate_bollinger(df)

    # 2. 震荡类指标
    df = calculate_rsi(df)
    df = calculate_kdj(df)

    # 3. 成交量指标
    df = calculate_volume_ma(df, [5, 20])
    df = calculate_obv(df)

    # 4. 生成综合信号
    df['trend_score'] = 0

    # 趋势得分
    df.loc[df['MA5'] > df['MA20'], 'trend_score'] += 1
    df.loc[df['MA20'] > df['MA60'], 'trend_score'] += 1
    df.loc[df['MACD_DIF'] > df['MACD_DEA'], 'trend_score'] += 1
    df.loc[df['close'] > df['BOLL_MID'], 'trend_score'] += 1

    # 震荡得分(超卖区为正，超买区为负)
    df.loc[df['RSI'] < 30, 'trend_score'] += 1
    df.loc[df['RSI'] > 70, 'trend_score'] -= 1
    df.loc[df['K'] < 20, 'trend_score'] += 1
    df.loc[df['K'] > 80, 'trend_score'] -= 1

    return df
```

## 4.6 可视化

```python
import matplotlib.pyplot as plt

def plot_technical_indicators(df, symbol='股票'):
    """绘制技术指标图表"""
    fig, axes = plt.subplots(4, 1, figsize=(15, 12))

    # 1. 价格与均线
    axes[0].plot(df.index, df['close'], label='收盘价', linewidth=1)
    axes[0].plot(df.index, df['MA5'], label='MA5', alpha=0.7)
    axes[0].plot(df.index, df['MA20'], label='MA20', alpha=0.7)
    axes[0].fill_between(df.index, df['BOLL_UP'], df['BOLL_LOW'], alpha=0.1)
    axes[0].set_title(f'{symbol} - 价格与均线')
    axes[0].legend()
    axes[0].grid(True)

    # 2. MACD
    axes[1].plot(df.index, df['MACD_DIF'], label='DIF', linewidth=1)
    axes[1].plot(df.index, df['MACD_DEA'], label='DEA', alpha=0.7)
    axes[1].bar(df.index, df['MACD_Hist'], alpha=0.3, label='Histogram')
    axes[1].set_title('MACD')
    axes[1].legend()
    axes[1].grid(True)

    # 3. RSI
    axes[2].plot(df.index, df['RSI'], label='RSI', linewidth=1)
    axes[2].axhline(70, color='r', linestyle='--', alpha=0.5)
    axes[2].axhline(30, color='g', linestyle='--', alpha=0.5)
    axes[2].set_title('RSI')
    axes[2].set_ylim(0, 100)
    axes[2].grid(True)

    # 4. 成交量
    colors = ['r' if close >= open_ else 'g'
              for close, open_ in zip(df['close'], df['open'])]
    axes[3].bar(df.index, df['volume'], color=colors, alpha=0.5)
    axes[3].plot(df.index, df['VMA20'], label='VMA20', color='blue')
    axes[3].set_title('成交量')
    axes[3].legend()
    axes[3].grid(True)

    plt.tight_layout()
    plt.show()
```

## 练习题

1. 实现ATR(真实波幅)指标
2. 编写多指标共振的选股策略
3. 计算技术指标的成功率
4. 实现动量指标(MTM)

## 学习检查清单

- [ ] 理解各类技术指标的原理
- [ ] 能够独立编写指标计算函数
- [ ] 掌握多指标组合使用方法
- [ ] 能够生成交易信号
- [ ] 掌握技术图表的绘制

## 下一步

技术指标掌握后 → [05-财务分析](../05-财务分析/) 或 [06-策略回测](../06-策略回测/)
