# 06-策略回测

## 目标

掌握策略回测的基本方法，评估策略有效性。

## 6.1 回测框架选择

| 框架 | 难度 | 特点 | 适用场景 |
|------|------|------|----------|
| Backtrader | ⭐⭐⭐ | 功能强大、社区活跃 | 复杂策略 |
| VeighNa | ⭐⭐⭐⭐ | 国内主流、功能全面 | 专业交易 |
| Zipline | ⭐⭐⭐ | Quantopian遗产 | 学术研究 |
| 自建框架 | ⭐⭐ | 学习推荐 | 理解原理 |

## 6.2 简单回测框架

```python
import pandas as pd
import numpy as np

class SimpleBacktest:
    """简单回测框架"""

    def __init__(self, data, initial_capital=100000):
        self.data = data.copy()
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0  # 持仓数量
        self.cash = initial_capital
        self.trades = []   # 交易记录

        # 准备数据
        if 'signal' not in self.data.columns:
            self.data['signal'] = 0

    def run(self, signal_column='signal'):
        """执行回测"""

        for i in range(1, len(self.data)):
            current_price = self.data['close'].iloc[i]
            signal = self.data[signal_column].iloc[i]

            # 买入信号
            if signal == 1 and self.position == 0:
                shares = int(self.cash / current_price)
                if shares > 0:
                    cost = shares * current_price
                    self.cash -= cost
                    self.position = shares
                    self.trades.append({
                        'date': self.data.index[i],
                        'action': 'buy',
                        'price': current_price,
                        'shares': shares,
                        'value': cost
                    })

            # 卖出信号
            elif signal == -1 and self.position > 0:
                proceeds = self.position * current_price
                self.cash += proceeds
                self.trades.append({
                    'date': self.data.index[i],
                    'action': 'sell',
                    'price': current_price,
                    'shares': self.position,
                    'value': proceeds
                })
                self.position = 0

    def get_results(self):
        """获取回测结果"""
        final_price = self.data['close'].iloc[-1]
        final_value = self.cash + self.position * final_price

        total_return = (final_value - self.initial_capital) / self.initial_capital

        return {
            'initial_capital': self.initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'final_cash': self.cash,
            'final_position': self.position,
            'trades': pd.DataFrame(self.trades)
        }

    def calculate_metrics(self):
        """计算回测指标"""
        results = self.get_results()
        trades_df = results['trades']

        if len(trades_df) == 0:
            return {}

        # 计算每笔交易收益
        buy_trades = trades_df[trades_df['action'] == 'buy']
        sell_trades = trades_df[trades_df['action'] == 'sell']

        # 配对买卖交易
        trade_returns = []
        for i in range(min(len(buy_trades), len(sell_trades))):
            buy_price = buy_trades.iloc[i]['price']
            sell_price = sell_trades.iloc[i]['price']
            ret = (sell_price - buy_price) / buy_price
            trade_returns.append(ret)

        metrics = {
            'total_return': results['total_return'],
            'total_trades': len(trades_df),
            'win_rate': sum(1 for r in trade_returns if r > 0) / len(trade_returns) if trade_returns else 0,
            'avg_return': np.mean(trade_returns) if trade_returns else 0,
            'max_return': max(trade_returns) if trade_returns else 0,
            'min_return': min(trade_returns) if trade_returns else 0
        }

        return metrics
```

## 6.3 双均线策略

```python
def double_ma_strategy(df, fast=5, slow=20):
    """双均线策略"""

    # 计算均线
    df['MA_fast'] = df['close'].rolling(fast).mean()
    df['MA_slow'] = df['close'].rolling(slow).mean()

    # 生成信号
    df['signal'] = 0

    # 金叉买入
    golden_cross = (df['MA_fast'] > df['MA_slow']) & \
                   (df['MA_fast'].shift(1) <= df['MA_slow'].shift(1))
    df.loc[golden_cross, 'signal'] = 1

    # 死叉卖出
    death_cross = (df['MA_fast'] < df['MA_slow']) & \
                  (df['MA_fast'].shift(1) >= df['MA_slow'].shift(1))
    df.loc[death_cross, 'signal'] = -1

    return df

# 使用示例
# df = double_ma_strategy(df)
# backtest = SimpleBacktest(df)
# backtest.run()
# results = backtest.get_results()
```

## 6.4 使用Backtrader

```python
import backtrader as bt

class DoubleMAStrategy(bt.Strategy):
    """Backtrader双均线策略"""

    params = (
        ('fast_period', 5),
        ('slow_period', 20),
    )

    def __init__(self):
        self.ma_fast = bt.indicators.SMA(self.data.close, period=self.params.fast_period)
        self.ma_slow = bt.indicators.SMA(self.data.close, period=self.params.slow_period)
        self.crossover = bt.indicators.CrossOver(self.ma_fast, self.ma_slow)

    def next(self):
        if self.crossover > 0:  # 金叉
            if not self.position:
                self.buy()
        elif self.crossover < 0:  # 死叉
            if self.position:
                self.sell()

def run_backtrader(df, initial_capital=100000):
    """运行Backtrader回测"""

    # 创建Cerebro引擎
    cerebro = bt.Cerebro()

    # 添加策略
    cerebro.addstrategy(DoubleMAStrategy)

    # 准备数据
    data = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(data)

    # 设置初始资金
    cerebro.broker.setcash(initial_capital)

    # 设置手续费
    cerebro.broker.setcommission(commission=0.001)

    # 添加分析器
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')

    # 运行回测
    results = cerebro.run()

    # 获取分析结果
    strat = results[0]
    print(f'夏普比率: {strat.analyzers.sharpe.get_analysis()["sharperatio"]:.2f}')
    print(f'最大回撤: {strat.analyzers.drawdown.get_analysis()["max"]["drawdown"]:.2f}%')
    print(f'总收益率: {strat.analyzers.returns.get_analysis()["rnorm100"]:.2f}%')

    # 绘图
    cerebro.plot()

    return cerebro
```

## 6.5 回测指标计算

```python
def calculate_backtest_metrics(df, initial_capital=100000):
    """计算详细回测指标"""

    # 基础收益
    df['returns'] = df['close'].pct_change()
    df['cumulative_returns'] = (1 + df['returns']).cumprod()

    # 年化收益率
    total_days = len(df)
    years = total_days / 252
    total_return = df['cumulative_returns'].iloc[-1] - 1
    annual_return = (1 + total_return) ** (1 / years) - 1

    # 波动率
    volatility = df['returns'].std() * np.sqrt(252)

    # 夏普比率 (假设无风险利率为3%)
    risk_free_rate = 0.03
    sharpe_ratio = (annual_return - risk_free_rate) / volatility

    # 最大回撤
    cum_returns = df['cumulative_returns']
    running_max = cum_returns.expanding().max()
    drawdown = (cum_returns - running_max) / running_max
    max_drawdown = drawdown.min()

    # 胜率
    df['trade_return'] = df['returns'].shift(-1)  # 次日收益
    win_rate = (df['trade_return'] > 0).sum() / (df['trade_return'] != 0).sum()

    # 盈亏比
    winning_returns = df[df['trade_return'] > 0]['trade_return'].mean()
    losing_returns = df[df['trade_return'] < 0]['trade_return'].mean()
    profit_loss_ratio = abs(winning_returns / losing_returns) if losing_returns != 0 else 0

    return {
        'total_return': total_return,
        'annual_return': annual_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'win_rate': win_rate,
        'profit_loss_ratio': profit_loss_ratio
    }
```

## 6.6 参数优化

```python
def optimize_ma_parameters(df, fast_range=(5, 20), slow_range=(20, 60)):
    """优化均线参数"""

    results = []

    for fast in range(fast_range[0], fast_range[1] + 1):
        for slow in range(slow_range[0], slow_range[1] + 1):
            if fast >= slow:
                continue

            # 运行策略
            df_temp = df.copy()
            df_temp = double_ma_strategy(df_temp, fast=fast, slow=slow)

            # 回测
            bt = SimpleBacktest(df_temp)
            bt.run()
            metrics = bt.calculate_metrics()

            results.append({
                'fast': fast,
                'slow': slow,
                'total_return': metrics.get('total_return', 0),
                'win_rate': metrics.get('win_rate', 0),
                'total_trades': metrics.get('total_trades', 0)
            })

    return pd.DataFrame(results).sort_values('total_return', ascending=False)

# 使用示例
# optimization_results = optimize_ma_parameters(df)
# print(optimization_results.head(10))
```

## 6.7 避免过拟合

```python
def walk_forward_analysis(df, train_period=252, test_period=63):
    """走向前分析(避免过拟合)"""

    results = []
    total_length = len(df)

    for start in range(0, total_length - train_period - test_period, test_period):
        train_end = start + train_period
        test_start = train_end
        test_end = test_start + test_period

        # 训练集：优化参数
        train_data = df.iloc[start:train_end]
        best_params = optimize_ma_parameters(train_data).iloc[0]

        # 测试集：验证
        test_data = df.iloc[test_start:test_end].copy()
        test_data = double_ma_strategy(
            test_data,
            fast=int(best_params['fast']),
            slow=int(best_params['slow'])
        )

        bt = SimpleBacktest(test_data)
        bt.run()
        metrics = bt.calculate_metrics()

        results.append({
            'train_start': start,
            'test_end': test_end,
            'fast': best_params['fast'],
            'slow': best_params['slow'],
            'test_return': metrics.get('total_return', 0)
        })

    return pd.DataFrame(results)
```

## 6.8 回测报告

```python
def generate_backtest_report(metrics, trades_df):
    """生成回测报告"""

    report = f"""
    ===== 回测报告 =====

    基础指标:
    ----------------
    初始资金: ¥{metrics.get('initial_capital', 0):,.2f}
    最终权益: ¥{metrics.get('final_value', 0):,.2f}
    总收益率: {metrics.get('total_return', 0)*100:.2f}%
    年化收益率: {metrics.get('annual_return', 0)*100:.2f}%

    风险指标:
    ----------------
    年化波动率: {metrics.get('volatility', 0)*100:.2f}%
    夏普比率: {metrics.get('sharpe_ratio', 0):.2f}
    最大回撤: {metrics.get('max_drawdown', 0)*100:.2f}%

    交易统计:
    ----------------
    总交易次数: {metrics.get('total_trades', 0)}
    胜率: {metrics.get('win_rate', 0)*100:.2f}%
    盈亏比: {metrics.get('profit_loss_ratio', 0):.2f}
    """

    print(report)
    return report
```

## 练习题

1. 实现布林带突破策略回测
2. 编写RSI超买超卖策略
3. 比较不同参数下的策略表现
4. 实现多因子选股策略回测

## 学习检查清单

- [ ] 理解回测的基本原理
- [ ] 能够编写简单回测框架
- [ ] 掌握Backtrader基础使用
- [ ] 能够计算回测评价指标
- [ ] 理解过拟合问题及解决方法

## 下一步

回测掌握后 → [07-实战项目](../07-实战项目/)
