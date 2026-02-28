"""
Python量化快速入门示例

本示例展示如何：
1. 获取股票数据
2. 计算技术指标
3. 生成交易信号
4. 运行回测
5. 分析结果
"""

# 安装依赖
# pip install akshare pandas matplotlib

import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt

# ==================== 第一步：获取数据 ====================
print("=" * 60)
print("第一步：获取股票数据")
print("=" * 60)

# 获取平安银行(000001)历史数据
stock_data = ak.stock_zh_a_hist(
    symbol="000001",       # 股票代码
    period="daily",        # 日线数据
    start_date="20230101", # 开始日期
    end_date="20240101",   # 结束日期
    adjust="qfq"           # 前复权
)

# 简单处理列名
stock_data.columns = [
    'date', 'open', 'close', 'high', 'low', 'volume',
    'amount', 'amplitude', 'pct_change', 'change', 'turnover'
]

# 设置日期为索引
stock_data['date'] = pd.to_datetime(stock_data['date'])
stock_data.set_index('date', inplace=True)

print(f"获取数据成功！共 {len(stock_data)} 条记录")
print("\n数据预览：")
print(stock_data[['open', 'close', 'high', 'low', 'volume']].head())

# ==================== 第二步：计算技术指标 ====================
print("\n" + "=" * 60)
print("第二步：计算技术指标")
print("=" * 60)

# 计算移动平均线
stock_data['MA5'] = stock_data['close'].rolling(5).mean()
stock_data['MA20'] = stock_data['close'].rolling(20).mean()

# 计算收益率
stock_data['returns'] = stock_data['close'].pct_change()

# 计算波动率
stock_data['volatility'] = stock_data['returns'].rolling(20).std()

print("技术指标计算完成！")
print("\n最新指标值：")
print(stock_data[['close', 'MA5', 'MA20', 'returns', 'volatility']].tail())

# ==================== 第三步：生成交易信号 ====================
print("\n" + "=" * 60)
print("第三步：生成交易信号")
print("=" * 60)

# 双均线策略信号
stock_data['signal'] = 0

# 金叉买入
golden_cross = (stock_data['MA5'] > stock_data['MA20']) & \
               (stock_data['MA5'].shift(1) <= stock_data['MA20'].shift(1))
stock_data.loc[golden_cross, 'signal'] = 1

# 死叉卖出
death_cross = (stock_data['MA5'] < stock_data['MA20']) & \
              (stock_data['MA5'].shift(1) >= stock_data['MA20'].shift(1))
stock_data.loc[death_cross, 'signal'] = -1

# 统计信号
buy_signals = (stock_data['signal'] == 1).sum()
sell_signals = (stock_data['signal'] == -1).sum()

print(f"生成信号完成！")
print(f"  买入信号: {buy_signals} 次")
print(f"  卖出信号: {sell_signals} 次")

# 显示最近的信号
recent_signals = stock_data[stock_data['signal'] != 0][['signal']]
print("\n最近的交易信号：")
print(recent_signals.tail(10))

# ==================== 第四步：简单回测 ====================
print("\n" + "=" * 60)
print("第四步：简单回测")
print("=" * 60)

initial_capital = 100000  # 初始资金10万
cash = initial_capital
position = 0  # 持仓数量
trades = []   # 交易记录

for i in range(1, len(stock_data)):
    price = stock_data['close'].iloc[i]
    signal = stock_data['signal'].iloc[i]
    date = stock_data.index[i]

    if signal == 1 and position == 0:  # 买入
        shares = int(cash / price)
        if shares > 0:
            cash -= shares * price
            position = shares
            trades.append({
                'date': date,
                'action': 'buy',
                'price': price,
                'shares': shares
            })

    elif signal == -1 and position > 0:  # 卖出
        cash += position * price
        trades.append({
            'date': date,
            'action': 'sell',
            'price': price,
            'shares': position
        })
        position = 0

# 最终价值
final_price = stock_data['close'].iloc[-1]
final_value = cash + position * final_price

# 计算收益
total_return = (final_value - initial_capital) / initial_capital

print(f"初始资金: ¥{initial_capital:,.2f}")
print(f"最终权益: ¥{final_value:,.2f}")
print(f"总收益率: {total_return*100:.2f}%")
print(f"交易次数: {len(trades)} 次")

# ==================== 第五步：可视化 ====================
print("\n" + "=" * 60)
print("第五步：生成图表")
print("=" * 60)

fig, axes = plt.subplots(3, 1, figsize=(14, 10))

# 1. 价格与均线
axes[0].plot(stock_data.index, stock_data['close'], label='收盘价', linewidth=1)
axes[0].plot(stock_data.index, stock_data['MA5'], label='MA5', alpha=0.7)
axes[0].plot(stock_data.index, stock_data['MA20'], label='MA20', alpha=0.7)
axes[0].set_title('平安银行 - 价格走势')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# 2. 收益率
axes[1].plot(stock_data.index, stock_data['returns'], label='日收益率')
axes[1].axhline(0, color='black', linestyle='--', alpha=0.5)
axes[1].set_title('日收益率')
axes[1].grid(True, alpha=0.3)

# 3. 波动率
axes[2].plot(stock_data.index, stock_data['volatility'], label='波动率(20日)', color='orange')
axes[2].set_title('波动率')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('quant_example.png', dpi=100)
print("图表已保存为 quant_example.png")

# ==================== 总结 ====================
print("\n" + "=" * 60)
print("学习建议")
print("=" * 60)
print("""
1. 熟悉本示例后，尝试修改参数：
   - 更改股票代码
   - 调整均线周期
   - 修改初始资金

2. 进阶练习：
   - 添加更多技术指标(RSI, MACD等)
   - 实现止损止盈逻辑
   - 计算夏普比率、最大回撤等指标

3. 继续学习：
   - notes/python-quant/00-环境准备/   - 环境配置
   - notes/python-quant/01-Python基础/  - Python语法
   - notes/python-quant/02-数据处理库/  - Pandas使用
   - notes/python-quant/03-金融数据获取/ - AkShare/Tushare
   - notes/python-quant/04-技术指标计算/ - 指标原理
   - notes/python-quant/05-财务分析/     - 财务数据处理
   - notes/python-quant/06-策略回测/     - 回测框架
   - notes/python-quant/07-实战项目/     - 综合项目
   - notes/python-quant/08-进阶方向/     - ML/DL/期权
""")

print("\n恭喜完成Python量化入门示例！")
print("=" * 60)
