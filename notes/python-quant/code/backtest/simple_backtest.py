"""
简单回测框架
"""

import pandas as pd
import numpy as np


class SimpleBacktest:
    """
    简单回测引擎

    支持基于信号的历史回测，计算基本回测指标
    """

    def __init__(self, data, initial_capital=100000, commission=0.001):
        """
        初始化回测引擎

        Parameters:
        -----------
        data : DataFrame
            包含价格和信号的数据
        initial_capital : float
            初始资金
        commission : float
            手续费率
        """
        self.data = data.copy()
        self.initial_capital = initial_capital
        self.commission = commission

        # 状态变量
        self.capital = initial_capital
        self.cash = initial_capital
        self.position = 0  # 持仓数量
        self.shares = 0    # 当前持仓股数

        # 记录
        self.trades = []
        self.daily_values = []
        self.positions = []

    def run(self, signal_column='signal', price_column='close'):
        """
        运行回测

        Parameters:
        -----------
        signal_column : str
            信号列名 (1=买入, -1=卖出, 0=持有)
        price_column : str
            价格列名
        """
        if signal_column not in self.data.columns:
            raise ValueError(f"数据中不存在信号列: {signal_column}")

        for i in range(len(self.data)):
            current_price = self.data[price_column].iloc[i]
            signal = self.data[signal_column].iloc[i]
            date = self.data.index[i]

            # 记录当日持仓价值
            total_value = self.cash + self.shares * current_price
            self.daily_values.append({
                'date': date,
                'cash': self.cash,
                'shares': self.shares,
                'price': current_price,
                'total_value': total_value
            })

            # 处理信号
            if signal == 1 and self.shares == 0:
                # 买入信号，空仓时买入
                self._buy(date, current_price)

            elif signal == -1 and self.shares > 0:
                # 卖出信号，有持仓时卖出
                self._sell(date, current_price)

    def _buy(self, date, price):
        """执行买入"""
        # 计算可买股数
        max_shares = int(self.cash / (price * (1 + self.commission)))

        if max_shares > 0:
            cost = max_shares * price * (1 + self.commission)
            self.cash -= cost
            self.shares = max_shares

            self.trades.append({
                'date': date,
                'action': 'buy',
                'price': price,
                'shares': max_shares,
                'cost': cost
            })

    def _sell(self, date, price):
        """执行卖出"""
        if self.shares > 0:
            proceeds = self.shares * price * (1 - self.commission)
            self.cash += proceeds

            self.trades.append({
                'date': date,
                'action': 'sell',
                'price': price,
                'shares': self.shares,
                'proceeds': proceeds
            })

            self.shares = 0

    def get_results(self):
        """获取回测结果"""
        df_values = pd.DataFrame(self.daily_values)
        df_values.set_index('date', inplace=True)

        final_value = df_values['total_value'].iloc[-1]
        total_return = (final_value - self.initial_capital) / self.initial_capital

        return {
            'initial_capital': self.initial_capital,
            'final_value': final_value,
            'total_return': total_return,
            'final_cash': self.cash,
            'final_shares': self.shares,
            'trades': pd.DataFrame(self.trades),
            'daily_values': df_values
        }

    def calculate_metrics(self, benchmark_returns=None):
        """
        计算回测指标

        Parameters:
        -----------
        benchmark_returns : Series
            基准收益率序列

        Returns:
        --------
        dict : 包含各项回测指标
        """
        results = self.get_results()
        daily_values = results['daily_values']

        # 计算日收益率
        daily_values['returns'] = daily_values['total_value'].pct_change()
        returns = daily_values['returns'].dropna()

        if len(returns) == 0:
            return {}

        # 基础指标
        total_return = results['total_return']
        trading_days = len(returns)
        years = trading_days / 252
        annual_return = (1 + total_return) ** (1 / years) - 1 if years > 0 else 0

        # 风险指标
        volatility = returns.std() * np.sqrt(252) if len(returns) > 1 else 0

        # 夏普比率 (假设无风险利率3%)
        risk_free_rate = 0.03
        sharpe_ratio = (annual_return - risk_free_rate) / volatility if volatility > 0 else 0

        # 最大回撤
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()

        # 交易统计
        trades_df = results['trades']
        buy_trades = trades_df[trades_df['action'] == 'buy']
        sell_trades = trades_df[trades_df['action'] == 'sell']

        # 配对交易计算盈亏
        paired_trades = min(len(buy_trades), len(sell_trades))
        trade_returns = []

        for i in range(paired_trades):
            buy_price = buy_trades.iloc[i]['price']
            sell_price = sell_trades.iloc[i]['price']
            trade_ret = (sell_price - buy_price) / buy_price
            trade_returns.append(trade_ret)

        # 胜率
        win_rate = sum(1 for r in trade_returns if r > 0) / len(trade_returns) if trade_returns else 0

        # 盈亏比
        winning_returns = [r for r in trade_returns if r > 0]
        losing_returns = [r for r in trade_returns if r < 0]

        avg_win = np.mean(winning_returns) if winning_returns else 0
        avg_loss = np.mean(losing_returns) if losing_returns else -1
        profit_loss_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0

        # 胜负比
        win_count = len(winning_returns)
        loss_count = len(losing_returns)
        win_loss_ratio = win_count / loss_count if loss_count > 0 else win_count

        metrics = {
            'total_return': total_return,
            'annual_return': annual_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'total_trades': len(trades_df),
            'trade_count': paired_trades,
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_loss_ratio': profit_loss_ratio,
            'win_loss_ratio': win_loss_ratio
        }

        # 如果有基准，计算相对指标
        if benchmark_returns is not None and len(benchmark_returns) == len(returns):
            benchmark_annual = benchmark_returns.mean() * 252
            excess_return = annual_return - benchmark_annual

            # 计算信息比率
            excess_returns = returns - benchmark_returns
            information_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(252) if excess_returns.std() > 0 else 0

            metrics.update({
                'benchmark_return': benchmark_annual,
                'excess_return': excess_return,
                'information_ratio': information_ratio
            })

        return metrics

    def print_report(self, benchmark_returns=None):
        """打印回测报告"""
        metrics = self.calculate_metrics(benchmark_returns)

        print("\n" + "="*50)
        print("回测报告".center(50))
        print("="*50)

        print("\n【收益指标】")
        print(f"总收益率:     {metrics['total_return']*100:8.2f}%")
        print(f"年化收益率:   {metrics['annual_return']*100:8.2f}%")

        print("\n【风险指标】")
        print(f"年化波动率:   {metrics['volatility']*100:8.2f}%")
        print(f"夏普比率:     {metrics['sharpe_ratio']:8.2f}")
        print(f"最大回撤:     {metrics['max_drawdown']*100:8.2f}%")

        print("\n【交易统计】")
        print(f"交易次数:     {metrics['total_trades']:8d}")
        print(f"完整交易:     {metrics['trade_count']:8d}")
        print(f"胜率:         {metrics['win_rate']*100:8.2f}%")
        print(f"平均盈利:     {metrics['avg_win']*100:8.2f}%")
        print(f"平均亏损:     {metrics['avg_loss']*100:8.2f}%")
        print(f"盈亏比:       {metrics['profit_loss_ratio']:8.2f}")
        print(f"胜负比:       {metrics['win_loss_ratio']:8.2f}")

        if 'excess_return' in metrics:
            print("\n【相对指标】")
            print(f"基准收益:     {metrics['benchmark_return']*100:8.2f}%")
            print(f"超额收益:     {metrics['excess_return']*100:8.2f}%")
            print(f"信息比率:     {metrics['information_ratio']:8.2f}")

        print("="*50 + "\n")


if __name__ == "__main__":
    # 测试代码
    import sys
    sys.path.append('..')
    from utils.data_helper import get_stock_data
    from indicators.technical_indicators import add_all_indicators

    print("测试回测框架...")

    # 获取数据
    data = get_stock_data("000001")
    if data is not None and len(data) > 60:
        # 添加技术指标
        data = add_all_indicators(data)

        # 生成简单信号：MA金叉买入，死叉卖出
        data['signal'] = 0
        golden_cross = (data['MA5'] > data['MA20']) & (data['MA5'].shift(1) <= data['MA20'].shift(1))
        death_cross = (data['MA5'] < data['MA20']) & (data['MA5'].shift(1) >= data['MA20'].shift(1))
        data.loc[golden_cross, 'signal'] = 1
        data.loc[death_cross, 'signal'] = -1

        # 运行回测
        backtest = SimpleBacktest(data)
        backtest.run()
        backtest.print_report()

        # 显示交易记录
        results = backtest.get_results()
        print("\n交易记录:")
        print(results['trades'])
    else:
        print("数据不足，无法回测")
