# 07-实战项目

## 目标

通过实际项目巩固所学知识，构建自己的量化工具。

## 项目列表

### 项目1：股票筛选器

**功能：** 根据财务和技术指标筛选股票

```python
import akshare as ak
import pandas as pd

class StockScreener:
    """股票筛选器"""

    def __init__(self):
        self.stock_list = self.get_stock_list()

    def get_stock_list(self):
        """获取股票列表"""
        return ak.stock_zh_a_spot_em()

    def screen_by_fundamentals(self, min_roe=15, max_pe=30, min_revenue_growth=10):
        """基本面筛选"""
        results = []

        for _, stock in self.stock_list.iterrows():
            symbol = stock['代码']
            name = stock['名称']

            try:
                # 获取财务指标
                indicator = ak.stock_financial_analysis_indicator(symbol=name)
                if indicator.empty:
                    continue

                latest = indicator.iloc[-1]

                # 筛选条件
                if (latest['净资产收益率'] >= min_roe and
                    stock['市盈率-动态'] != '-' and
                    float(stock['市盈率-动态']) <= max_pe and
                    latest['营业收入增长率'] >= min_revenue_growth):

                    results.append({
                        'code': symbol,
                        'name': name,
                        'roe': latest['净资产收益率'],
                        'pe': stock['市盈率-动态'],
                        'revenue_growth': latest['营业收入增长率'],
                        'price': stock['最新价']
                    })

            except Exception:
                continue

        return pd.DataFrame(results)

    def screen_by_technical(self, period=20):
        """技术面筛选"""
        results = []

        for _, stock in self.stock_list.head(100).iterrows():
            symbol = stock['代码']

            try:
                # 获取历史数据
                data = ak.stock_zh_a_hist(
                    symbol=symbol,
                    period="daily",
                    start_date="20240101",
                    adjust="qfq"
                )

                if len(data) < period:
                    continue

                # 计算均线
                data['MA20'] = data['收盘'].rolling(20).mean()
                data['MA60'] = data['收盘'].rolling(60).mean()

                latest = data.iloc[-1]

                # 金叉筛选
                if (latest['收盘'] > latest['MA20'] and
                    latest['MA20'] > latest['MA60']):

                    results.append({
                        'code': symbol,
                        'name': stock['名称'],
                        'price': latest['收盘'],
                        'MA20': latest['MA20'],
                        'MA60': latest['MA60']
                    })

            except Exception:
                continue

        return pd.DataFrame(results)

# 使用
# screener = StockScreener()
# fundamental_stocks = screener.screen_by_fundamentals()
# technical_stocks = screener.screen_by_technical()
```

### 项目2：投资组合分析

```python
class PortfolioAnalyzer:
    """投资组合分析"""

    def __init__(self, holdings):
        """
        holdings: dict of {'symbol': shares}
        """
        self.holdings = holdings
        self.prices = self.get_prices()

    def get_prices(self):
        """获取最新价格"""
        price_data = {}
        for symbol in self.holdings.keys():
            try:
                data = ak.stock_zh_a_hist(symbol=symbol, period="daily", adjust="qfq")
                if not data.empty:
                    price_data[symbol] = data.iloc[-1]['收盘']
            except:
                pass
        return price_data

    def calculate_portfolio_value(self):
        """计算组合价值"""
        total_value = 0
        details = []

        for symbol, shares in self.holdings.items():
            if symbol in self.prices:
                value = shares * self.prices[symbol]
                total_value += value
                details.append({
                    'symbol': symbol,
                    'shares': shares,
                    'price': self.prices[symbol],
                    'value': value
                })

        return {
            'total_value': total_value,
            'holdings': pd.DataFrame(details)
        }

    def calculate_weights(self):
        """计算持仓权重"""
        portfolio = self.calculate_portfolio_value()
        total = portfolio['total_value']
        holdings_df = portfolio['holdings']

        holdings_df['weight'] = holdings_df['value'] / total

        return holdings_df

    def calculate_returns(self, period=20):
        """计算组合收益"""
        returns_data = {}

        for symbol in self.holdings.keys():
            try:
                data = ak.stock_zh_a_hist(symbol=symbol, period="daily", adjust="qfq")
                if len(data) > period:
                    data['returns'] = data['收盘'].pct_change()
                    returns_data[symbol] = data['returns'].iloc[-period:]
            except:
                pass

        returns_df = pd.DataFrame(returns_data)

        # 计算组合收益
        weights = self.calculate_weights()
        weights_dict = dict(zip(weights['symbol'], weights['weight']))

        portfolio_returns = pd.Series(index=returns_df.index, dtype=float)
        for date in returns_df.index:
            daily_return = 0
            for symbol in returns_df.columns:
                if symbol in weights_dict:
                    daily_return += returns_df.loc[date, symbol] * weights_dict[symbol]
            portfolio_returns[date] = daily_return

        # 计算累计收益
        cumulative_return = (1 + portfolio_returns).prod() - 1

        return {
            'daily_returns': portfolio_returns,
            'cumulative_return': cumulative_return,
            'volatility': portfolio_returns.std() * (252 ** 0.5)
        }
```

### 项目3：策略监控系统

```python
import time
from datetime import datetime

class StrategyMonitor:
    """策略监控"""

    def __init__(self, watchlist):
        self.watchlist = watchlist  # 监控股票列表
        self.signals = []

    def check_signals(self):
        """检查交易信号"""
        new_signals = []

        for symbol in self.watchlist:
            try:
                data = ak.stock_zh_a_hist(symbol=symbol, period="daily", adjust="qfq")
                if len(data) < 60:
                    continue

                # 计算指标
                data['MA5'] = data['收盘'].rolling(5).mean()
                data['MA20'] = data['收盘'].rolling(20).mean()
                data['RSI'] = self.calculate_rsi(data['收盘'])

                latest = data.iloc[-1]
                prev = data.iloc[-2]

                # 金叉信号
                if (prev['收盘'] <= prev['MA20'] and
                    latest['收盘'] > latest['MA20']):
                    new_signals.append({
                        'time': datetime.now(),
                        'symbol': symbol,
                        'type': 'BUY',
                        'reason': 'MA金叉',
                        'price': latest['收盘']
                    })

                # 死叉信号
                if (prev['收盘'] >= prev['MA20'] and
                    latest['收盘'] < latest['MA20']):
                    new_signals.append({
                        'time': datetime.now(),
                        'symbol': symbol,
                        'type': 'SELL',
                        'reason': 'MA死叉',
                        'price': latest['收盘']
                    })

                # RSI超卖
                if latest['RSI'] < 30 and prev['RSI'] >= 30:
                    new_signals.append({
                        'time': datetime.now(),
                        'symbol': symbol,
                        'type': 'BUY',
                        'reason': 'RSI超卖',
                        'price': latest['收盘']
                    })

            except Exception as e:
                continue

        self.signals.extend(new_signals)
        return new_signals

    def calculate_rsi(self, prices, period=14):
        """计算RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def run_monitor(self, interval=300):
        """运行监控"""
        print(f"开始监控 {len(self.watchlist)} 只股票...")

        while True:
            signals = self.check_signals()

            if signals:
                print(f"\n{datetime.now().strftime('%H:%M:%S')} 发现新信号:")
                for signal in signals:
                    print(f"  {signal['symbol']} - {signal['type']} - {signal['reason']} @ {signal['price']}")

            time.sleep(interval)
```

### 项目4：财务报表分析器

```python
class FinancialAnalyzer:
    """财务报表分析器"""

    def analyze_company(self, symbol, name):
        """全面分析公司财务"""

        # 获取数据
        balance, profit, cashflow, indicator = self.get_financial_data(symbol, name)

        analysis = {
            'basic_info': self.get_basic_info(symbol),
            'profitability': self.analyze_profitability(indicator),
            'growth': self.analyze_growth(indicator),
            'valuation': self.analyze_valuation(symbol, indicator),
            'cash_flow': self.analyze_cash_flow(cashflow),
            'health': self.analyze_financial_health(balance, indicator)
        }

        return analysis

    def generate_report(self, analysis):
        """生成分析报告"""
        report = f"""
        ===== 财务分析报告 =====

        基本信息:
        --------
        {analysis['basic_info']}

        盈利能力:
        --------
        {analysis['profitability']}

        成长能力:
        --------
        {analysis['growth']}

        估值分析:
        --------
        {analysis['valuation']}

        现金流分析:
        --------
        {analysis['cash_flow']}

        财务健康:
        --------
        {analysis['health']}
        """
        return report
```

## 实战建议

1. **从小项目开始**
   - 先完成单一功能的工具
   - 逐步增加复杂度

2. **记录学习过程**
   - 在对应目录记录笔记
   - 保存代码示例

3. **建立代码库**
   - 复用常用函数
   - 建立自己的工具包

4. **持续优化**
   - 定期回顾代码
   - 优化性能和逻辑

## 学习检查清单

- [ ] 完成至少2个实战项目
- [ ] 建立个人代码库
- [ ] 能够独立完成数据分析
- [ ] 掌握回测流程
- [ ] 理解策略开发思路

## 下一步

完成实战项目后 → [08-进阶方向](../08-进阶方向/)
