"""
技术指标计算函数
"""

import pandas as pd
import numpy as np


def ma(data, period):
    """
    简单移动平均线

    Parameters:
    -----------
    data : Series
        价格序列
    period : int
        周期

    Returns:
    --------
    Series : MA值
    """
    return data.rolling(window=period).mean()


def ema(data, period):
    """
    指数移动平均线

    Parameters:
    -----------
    data : Series
        价格序列
    period : int
        周期

    Returns:
    --------
    Series : EMA值
    """
    return data.ewm(span=period, adjust=False).mean()


def macd(data, fast=12, slow=26, signal=9):
    """
    MACD指标

    Parameters:
    -----------
    data : Series
        收盘价序列
    fast : int
        快线周期
    slow : int
        慢线周期
    signal : int
        信号线周期

    Returns:
    --------
    DataFrame : 包含DIF, DEA, MACD柱
    """
    ema_fast = data.ewm(span=fast, adjust=False).mean()
    ema_slow = data.ewm(span=slow, adjust=False).mean()

    dif = ema_fast - ema_slow
    dea = dif.ewm(span=signal, adjust=False).mean()
    macd_hist = (dif - dea) * 2

    return pd.DataFrame({
        'DIF': dif,
        'DEA': dea,
        'MACD': macd_hist
    })


def bollinger_bands(data, period=20, std_dev=2):
    """
    布林带

    Parameters:
    -----------
    data : Series
        收盘价序列
    period : int
        周期
    std_dev : float
        标准差倍数

    Returns:
    --------
    DataFrame : 包含上轨、中轨、下轨
    """
    middle = data.rolling(window=period).mean()
    std = data.rolling(window=period).std()

    upper = middle + std_dev * std
    lower = middle - std_dev * std

    return pd.DataFrame({
        'BOLL_UPPER': upper,
        'BOLL_MIDDLE': middle,
        'BOLL_LOWER': lower
    })


def rsi(data, period=14):
    """
    RSI相对强弱指标

    Parameters:
    -----------
    data : Series
        收盘价序列
    period : int
        周期

    Returns:
    --------
    Series : RSI值
    """
    delta = data.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def kdj(data, n=9, m1=3, m2=3):
    """
    KDJ指标

    Parameters:
    -----------
    data : DataFrame
        包含high, low, close列
    n : int
        RSV周期
    m1 : int
        K值平滑周期
    m2 : int
        D值平滑周期

    Returns:
    --------
    DataFrame : 包含K, D, J值
    """
    low_list = data['low'].rolling(window=n).min()
    high_list = data['high'].rolling(window=n).max()

    rsv = (data['close'] - low_list) / (high_list - low_list) * 100

    k = rsv.ewm(com=m1-1, adjust=False).mean()
    d = k.ewm(com=m2-1, adjust=False).mean()
    j = 3 * k - 2 * d

    return pd.DataFrame({
        'K': k,
        'D': d,
        'J': j
    })


def atr(data, period=14):
    """
    ATR真实波幅

    Parameters:
    -----------
    data : DataFrame
        包含high, low, close列
    period : int
        周期

    Returns:
    --------
    Series : ATR值
    """
    high = data['high']
    low = data['low']
    close = data['close']

    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()

    return atr


def obv(data):
    """
    OBV能量潮

    Parameters:
    -----------
    data : DataFrame
        包含close和volume列

    Returns:
    --------
    Series : OBV值
    """
    close = data['close']
    volume = data['volume']

    obv = pd.Series(index=close.index, dtype=float)
    obv.iloc[0] = volume.iloc[0]

    for i in range(1, len(close)):
        if close.iloc[i] > close.iloc[i-1]:
            obv.iloc[i] = obv.iloc[i-1] + volume.iloc[i]
        elif close.iloc[i] < close.iloc[i-1]:
            obv.iloc[i] = obv.iloc[i-1] - volume.iloc[i]
        else:
            obv.iloc[i] = obv.iloc[i-1]

    return obv


def volume_ma(data, periods=[5, 10, 20]):
    """
    成交量均线

    Parameters:
    -----------
    data : Series
        成交量序列
    periods : list
        周期列表

    Returns:
    --------
    DataFrame : 包含各周期VMA
    """
    result = {}
    for period in periods:
        result[f'VMA{period}'] = data.rolling(window=period).mean()

    return pd.DataFrame(result)


def williams_r(data, period=14):
    """
    威廉指标

    Parameters:
    -----------
    data : DataFrame
        包含high, low, close列
    period : int
        周期

    Returns:
    --------
    Series : WR值
    """
    high_high = data['high'].rolling(window=period).max()
    low_low = data['low'].rolling(window=period).min()

    wr = (high_high - data['close']) / (high_high - low_low) * -100

    return wr


def add_all_indicators(data):
    """
    添加所有技术指标到数据框

    Parameters:
    -----------
    data : DataFrame
        包含OHLCV数据

    Returns:
    --------
    DataFrame : 添加指标后的数据
    """
    df = data.copy()

    # 趋势指标
    df['MA5'] = ma(df['close'], 5)
    df['MA10'] = ma(df['close'], 10)
    df['MA20'] = ma(df['close'], 20)
    df['MA60'] = ma(df['close'], 60)

    # MACD
    macd_df = macd(df['close'])
    df['MACD_DIF'] = macd_df['DIF']
    df['MACD_DEA'] = macd_df['DEA']
    df['MACD'] = macd_df['MACD']

    # 布林带
    boll = bollinger_bands(df['close'])
    df['BOLL_UPPER'] = boll['BOLL_UPPER']
    df['BOLL_MIDDLE'] = boll['BOLL_MIDDLE']
    df['BOLL_LOWER'] = boll['BOLL_LOWER']

    # 震荡指标
    df['RSI'] = rsi(df['close'])

    kdj_df = kdj(df)
    df['K'] = kdj_df['K']
    df['D'] = kdj_df['D']
    df['J'] = kdj_df['J']

    df['WR'] = williams_r(df)

    # 波动率
    df['ATR'] = atr(df)

    # 成交量指标
    vma = volume_ma(df['volume'])
    for col in vma.columns:
        df[col] = vma[col]

    df['OBV'] = obv(df)

    return df


if __name__ == "__main__":
    # 测试代码
    import sys
    sys.path.append('..')
    from utils.data_helper import get_stock_data

    print("测试技术指标计算...")

    # 获取测试数据
    data = get_stock_data("000001")
    if data is not None and len(data) > 60:
        # 添加指标
        data_with_indicators = add_all_indicators(data)

        print(f"\n计算完成，数据列: {list(data_with_indicators.columns)}")
        print("\n最近5天数据:")
        print(data_with_indicators[['close', 'MA5', 'MA20', 'RSI', 'MACD_DIF']].tail())
    else:
        print("数据不足，无法计算指标")
