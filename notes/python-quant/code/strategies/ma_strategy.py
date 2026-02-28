"""
交易策略示例
"""

import pandas as pd
import numpy as np


def double_ma_strategy(data, fast=5, slow=20):
    """
    双均线策略

    信号规则:
    - 快线上穿慢线(金叉) -> 买入信号
    - 快线下穿慢线(死叉) -> 卖出信号

    Parameters:
    -----------
    data : DataFrame
        包含OHLCV数据
    fast : int
        快线周期
    slow : int
        慢线周期

    Returns:
    --------
    DataFrame : 添加信号后的数据
    """
    df = data.copy()

    # 计算均线
    df[f'MA{fast}'] = df['close'].rolling(fast).mean()
    df[f'MA{slow}'] = df['close'].rolling(slow).mean()

    # 初始化信号
    df['signal'] = 0

    # 金叉: 快线上穿慢线
    golden_cross = (df[f'MA{fast}'] > df[f'MA{slow}']) & \
                   (df[f'MA{fast}'].shift(1) <= df[f'MA{slow}'].shift(1))

    # 死叉: 快线下穿慢线
    death_cross = (df[f'MA{fast}'] < df[f'MA{slow}']) & \
                  (df[f'MA{fast}'].shift(1) >= df[f'MA{slow}'].shift(1))

    df.loc[golden_cross, 'signal'] = 1   # 买入
    df.loc[death_cross, 'signal'] = -1   # 卖出

    return df


def triple_ma_strategy(data, short=5, medium=20, long=60):
    """
    三均线策略

    信号规则:
    - 短线 > 中线 > 长线 -> 买入
    - 短线 < 中线 < 长线 -> 卖出

    Parameters:
    -----------
    data : DataFrame
        包含OHLCV数据
    short : int
        短线周期
    medium : int
        中线周期
    long : int
        长线周期

    Returns:
    --------
    DataFrame : 添加信号后的数据
    """
    df = data.copy()

    # 计算三条均线
    df[f'MA{short}'] = df['close'].rolling(short).mean()
    df[f'MA{medium}'] = df['close'].rolling(medium).mean()
    df[f'MA{long}'] = df['close'].rolling(long).mean()

    df['signal'] = 0

    # 多头排列
    bullish = (df[f'MA{short}'] > df[f'MA{medium}']) & \
              (df[f'MA{medium}'] > df[f'MA{long}']) & \
              (df[f'MA{short}'].shift(1) <= df[f'MA{medium}'].shift(1))

    # 空头排列
    bearish = (df[f'MA{short}'] < df[f'MA{medium}']) & \
              (df[f'MA{medium}'] < df[f'MA{long}']) & \
              (df[f'MA{short}'].shift(1) >= df[f'MA{medium}'].shift(1))

    df.loc[bullish, 'signal'] = 1
    df.loc[bearish, 'signal'] = -1

    return df


def macd_strategy(data, fast=12, slow=26, signal=9):
    """
    MACD策略

    信号规则:
    - DIF上穿DEA(金叉) -> 买入
    - DIF下穿DEA(死叉) -> 卖出

    Parameters:
    -----------
    data : DataFrame
        包含OHLCV数据
    fast : int
        快线周期
    slow : int
        慢线周期
    signal : int
        信号线周期

    Returns:
    --------
    DataFrame : 添加信号后的数据
    """
    df = data.copy()

    # 计算MACD
    ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow, adjust=False).mean()

    df['DIF'] = ema_fast - ema_slow
    df['DEA'] = df['DIF'].ewm(span=signal, adjust=False).mean()
    df['MACD'] = (df['DIF'] - df['DEA']) * 2

    df['signal'] = 0

    # 金叉
    golden_cross = (df['DIF'] > df['DEA']) & (df['DIF'].shift(1) <= df['DEA'].shift(1))
    # 死叉
    death_cross = (df['DIF'] < df['DEA']) & (df['DIF'].shift(1) >= df['DEA'].shift(1))

    df.loc[golden_cross, 'signal'] = 1
    df.loc[death_cross, 'signal'] = -1

    return df


def bollinger_bands_strategy(data, period=20, std_dev=2):
    """
    布林带策略

    信号规则:
    - 价格触及下轨 -> 买入
    - 价格触及上轨 -> 卖出
    - 价格突破中轨 -> 加仓

    Parameters:
    -----------
    data : DataFrame
        包含OHLCV数据
    period : int
        均线周期
    std_dev : float
        标准差倍数

    Returns:
    --------
    DataFrame : 添加信号后的数据
    """
    df = data.copy()

    # 计算布林带
    middle = df['close'].rolling(period).mean()
    std = df['close'].rolling(period).std()

    df['BOLL_UPPER'] = middle + std_dev * std
    df['BOLL_MIDDLE'] = middle
    df['BOLL_LOWER'] = middle - std_dev * std

    df['signal'] = 0

    # 触及下轨
    touch_lower = (df['close'] <= df['BOLL_LOWER']) & \
                  (df['close'].shift(1) > df['BOLL_LOWER'].shift(1))

    # 触及上轨
    touch_upper = (df['close'] >= df['BOLL_UPPER']) & \
                  (df['close'].shift(1) < df['BOLL_UPPER'].shift(1))

    df.loc[touch_lower, 'signal'] = 1
    df.loc[touch_upper, 'signal'] = -1

    return df


def rsi_strategy(data, period=14, oversold=30, overbought=70):
    """
    RSI策略

    信号规则:
    - RSI < 超卖线 -> 买入
    - RSI > 超买线 -> 卖出

    Parameters:
    -----------
    data : DataFrame
        包含OHLCV数据
    period : int
        RSI周期
    oversold : float
        超卖阈值
    overbought : float
        超买阈值

    Returns:
    --------
    DataFrame : 添加信号后的数据
    """
    df = data.copy()

    # 计算RSI
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    df['signal'] = 0

    # 超卖区
    oversold_signal = (df['RSI'] < oversold) & (df['RSI'].shift(1) >= oversold)
    # 超买区
    overbought_signal = (df['RSI'] > overbought) & (df['RSI'].shift(1) <= overbought)

    df.loc[oversold_signal, 'signal'] = 1
    df.loc[overbought_signal, 'signal'] = -1

    return df


def multi_indicator_strategy(data):
    """
    多指标共振策略

    多个指标同时发出信号才交易

    Parameters:
    -----------
    data : DataFrame
        包含OHLCV数据

    Returns:
    --------
    DataFrame : 添加信号后的数据
    """
    df = data.copy()

    # 计算各指标
    df = double_ma_strategy(df, fast=5, slow=20)
    ma_signal = df['signal']

    df = macd_strategy(df)
    macd_signal = df['signal']

    df = rsi_strategy(df)
    rsi_signal = df['signal']

    # 综合信号: 至少两个指标同向才发出信号
    df['final_signal'] = 0

    # 买入信号: 至少两个指标看多
    buy_condition = (ma_signal == 1).astype(int) + \
                    (macd_signal == 1).astype(int) + \
                    (rsi_signal == 1).astype(int)
    df.loc[buy_condition >= 2, 'final_signal'] = 1

    # 卖出信号: 至少两个指标看空
    sell_condition = (ma_signal == -1).astype(int) + \
                     (macd_signal == -1).astype(int) + \
                     (rsi_signal == -1).astype(int)
    df.loc[sell_condition >= 2, 'final_signal'] = -1

    # 替换signal列
    df['signal'] = df['final_signal']
    df = df.drop('final_signal', axis=1)

    return df


def momentum_strategy(data, period=20, threshold=0.02):
    """
    动量策略

    信号规则:
    - 过去N天涨幅超过阈值 -> 买入
    - 过去N天跌幅超过阈值 -> 卖出

    Parameters:
    -----------
    data : DataFrame
        包含OHLCV数据
    period : int
        动量计算周期
    threshold : float
        涨跌幅阈值

    Returns:
    --------
    DataFrame : 添加信号后的数据
    """
    df = data.copy()

    # 计算动量
    df['momentum'] = df['close'].pct_change(period)

    df['signal'] = 0

    # 强势动量
    df.loc[df['momentum'] > threshold, 'signal'] = 1
    # 弱势动量
    df.loc[df['momentum'] < -threshold, 'signal'] = -1

    return df


if __name__ == "__main__":
    # 测试代码
    import sys
    sys.path.append('..')
    from utils.data_helper import get_stock_data
    from backtest.simple_backtest import SimpleBacktest

    print("测试交易策略...")

    # 获取数据
    data = get_stock_data("000001")
    if data is not None and len(data) > 60:
        strategies = [
            ("双均线策略", lambda df: double_ma_strategy(df)),
            ("MACD策略", lambda df: macd_strategy(df)),
            ("RSI策略", lambda df: rsi_strategy(df)),
            ("布林带策略", lambda df: bollinger_bands_strategy(df)),
            ("多指标策略", lambda df: multi_indicator_strategy(df))
        ]

        results_summary = []

        for name, strategy_func in strategies:
            print(f"\n{'='*40}")
            print(f"回测策略: {name}")
            print('='*40)

            # 应用策略
            data_with_signal = strategy_func(data.copy())

            # 回测
            backtest = SimpleBacktest(data_with_signal)
            backtest.run()
            backtest.print_report()

            # 记录结果
            metrics = backtest.calculate_metrics()
            results_summary.append({
                'strategy': name,
                'total_return': metrics['total_return'],
                'sharpe_ratio': metrics['sharpe_ratio'],
                'max_drawdown': metrics['max_drawdown'],
                'win_rate': metrics['win_rate'],
                'trade_count': metrics['trade_count']
            })

        # 策略对比
        print("\n" + "="*80)
        print("策略对比汇总".center(80))
        print("="*80)
        summary_df = pd.DataFrame(results_summary)
        print(summary_df.to_string(index=False))
        print("="*80)
    else:
        print("数据不足，无法测试策略")
