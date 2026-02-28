# 05-财务分析

## 目标

使用Python自动化分析上市公司财务数据，评估投资价值。

## 5.1 财务数据获取与处理

```python
import akshare as ak
import pandas as pd

def get_financial_statements(symbol, name):
    """获取三张财务报表"""

    # 资产负债表
    balance = ak.stock_balance_sheet_by_report_em(symbol=name)

    # 利润表
    profit = ak.stock_profit_sheet_by_report_em(symbol=name)

    # 现金流量表
    cashflow = ak.stock_cash_flow_sheet_by_report_em(symbol=name)

    # 财务指标
    indicator = ak.stock_financial_analysis_indicator(symbol=name)

    return balance, profit, cashflow, indicator

# 使用示例
balance, profit, cashflow, indicator = get_financial_statements("600519", "贵州茅台")
```

## 5.2 关键财务指标计算

### 盈利能力指标

```python
def calculate_profitability(indicator):
    """计算盈利能力指标"""

    df = indicator.copy()

    # ROE - 净资产收益率
    if '净资产收益率' in df.columns:
        df['ROE'] = df['净资产收益率'] / 100

    # ROA - 总资产收益率
    if '总资产净利率' in df.columns:
        df['ROA'] = df['总资产净利率'] / 100

    # 毛利率
    if '销售毛利率' in df.columns:
        df['Gross_Margin'] = df['销售毛利率'] / 100

    # 净利率
    if '销售净利率' in df.columns:
        df['Net_Margin'] = df['销售净利率'] / 100

    return df
```

### 偿债能力指标

```python
def calculate_solvency(balance):
    """计算偿债能力指标"""

    df = balance.copy()

    # 流动比率
    if '流动资产合计' in df.columns and '流动负债合计' in df.columns:
        df['Current_Ratio'] = df['流动资产合计'] / df['流动负债合计']

    # 速动比率
    if '速动资产' in df.columns and '流动负债合计' in df.columns:
        df['Quick_Ratio'] = df['速动资产'] / df['流动负债合计']

    # 资产负债率
    if '负债合计' in df.columns and '资产总计' in df.columns:
        df['Debt_Ratio'] = df['负债合计'] / df['资产总计']

    return df
```

### 运营能力指标

```python
def calculate_efficiency(balance, profit):
    """计算运营能力指标"""

    # 应收账款周转率
    if '营业收入' in profit.columns and '应收账款' in balance.columns:
        # 需要合并数据计算
        pass

    # 存货周转率
    if '营业成本' in profit.columns and '存货' in balance.columns:
        # 存货周转率 = 营业成本 / 平均存货
        pass

    # 总资产周转率
    if '营业收入' in profit.columns and '资产总计' in balance.columns:
        pass

    return df
```

### 成长能力指标

```python
def calculate_growth(financial_data):
    """计算成长能力指标"""

    df = financial_data.copy()

    # 营收增长率
    if '营业收入' in df.columns:
        df['Revenue_Growth'] = df['营业收入'].pct_change()

    # 净利润增长率
    if '净利润' in df.columns:
        df['Profit_Growth'] = df['净利润'].pct_change()

    # 总资产增长率
    if '总资产' in df.columns:
        df['Asset_Growth'] = df['总资产'].pct_change()

    return df
```

## 5.3 估值指标分析

```python
def get_valuation_metrics(symbol):
    """获取估值指标"""

    # 获取实时行情数据
    stock_info = ak.stock_zh_a_spot_em()
    stock_data = stock_info[stock_info['代码'] == symbol].iloc[0]

    metrics = {
        'code': symbol,
        'price': stock_data['最新价'],
        'pe': stock_data['市盈率-动态'],
        'pb': stock_data['市净率'],
        'market_cap': stock_data['总市值'],
        'circulation_cap': stock_data['流通市值']
    }

    return metrics
```

### PE百分位分析

```python
def calculate_pe_percentile(symbol, years=5):
    """计算PE历史百分位"""

    # 获取历史数据
    import datetime
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=years*365)

    # 这里需要历史PE数据
    # 实际应用中可以用tushare或自建数据库
    # pe_history = get_historical_pe(symbol, start_date, end_date)

    # 计算百分位
    # current_pe = get_current_pe(symbol)
    # percentile = (pe_history < current_pe).sum() / len(pe_history) * 100

    # return percentile
    pass
```

## 5.4 综合财务评分

```python
def financial_score(symbol, name):
    """综合财务评分"""

    # 获取数据
    _, _, _, indicator = get_financial_statements(symbol, name)
    valuation = get_valuation_metrics(symbol)

    score = 0
    max_score = 100

    # 1. ROE评分 (20分)
    # ROE > 20%得满分，10%以下不得分
    roe = indicator.iloc[-1]['净资产收益率']
    if roe >= 20:
        score += 20
    elif roe >= 10:
        score += (roe - 10) * 2

    # 2. 毛利率评分 (15分)
    # 毛利率 > 50%得满分
    gross_margin = indicator.iloc[-1]['销售毛利率']
    if gross_margin >= 50:
        score += 15
    elif gross_margin >= 20:
        score += (gross_margin - 20) * 0.5

    # 3. 净利率评分 (15分)
    net_margin = indicator.iloc[-1]['销售净利率']
    if net_margin >= 20:
        score += 15
    elif net_margin >= 5:
        score += (net_margin - 5) * 1

    # 4. 成长性评分 (20分)
    revenue_growth = indicator.iloc[-1]['营业收入增长率']
    profit_growth = indicator.iloc[-1]['净利润增长率']

    if revenue_growth > 20 and profit_growth > 20:
        score += 20
    elif revenue_growth > 0 and profit_growth > 0:
        score += 10

    # 5. 估值评分 (20分)
    pe = valuation['pe']
    if 0 < pe < 15:
        score += 20
    elif 15 <= pe < 30:
        score += (30 - pe) * 1.33

    # 6. 偿债能力 (10分)
    debt_ratio = indicator.iloc[-1]['资产负债率']
    if debt_ratio < 30:
        score += 10
    elif debt_ratio < 60:
        score += (60 - debt_ratio) * 0.33

    return {
        'symbol': symbol,
        'name': name,
        'total_score': score,
        'max_score': max_score,
        'rating': 'A' if score >= 80 else 'B' if score >= 60 else 'C'
    }
```

## 5.5 财务异常检测

```python
def detect_financial_anomaly(balance, profit, cashflow):
    """检测财务异常"""

    alerts = []

    # 1. 净利润与经营现金流不匹配
    if '净利润' in profit.columns and '经营活动产生的现金流量净额' in cashflow.columns:
        net_income = profit.iloc[-1]['净利润']
        operating_cash = cashflow.iloc[-1]['经营活动产生的现金流量净额']

        # 如果净利润很高但经营现金流为负
        if net_income > 0 and operating_cash < 0:
            alerts.append("警告：净利润为正但经营现金流为负")

    # 2. 应收账款异常增长
    if '应收账款' in balance.columns:
        receivables = balance['应收账款']
        receivables_growth = receivables.pct_change().iloc[-1]

        if receivables_growth > 0.5:  # 增长超过50%
            alerts.append(f"警告：应收账款增长{receivables_growth*100:.1f}%")

    # 3. 存货异常增长
    if '存货' in balance.columns:
        inventory = balance['存货']
        inventory_growth = inventory.pct_change().iloc[-1]

        if inventory_growth > 0.3:
            alerts.append(f"警告：存货增长{inventory_growth*100:.1f}%")

    # 4. 高负债高存贷双高
    if '货币资金' in balance.columns and '短期借款' in balance.columns:
        cash = balance.iloc[-1]['货币资金']
        short_debt = balance.iloc[-1]['短期借款']

        if cash > 0 and short_debt > cash * 0.5:
            alerts.append("警告：高存款高借款异常")

    return alerts
```

## 5.6 财务可视化

```python
import matplotlib.pyplot as plt

def plot_financial_trends(symbol, name):
    """绘制财务趋势图"""

    _, profit, _, indicator = get_financial_statements(symbol, name)

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    # 1. 营收与利润趋势
    axes[0, 0].plot(profit['报告期'], profit['营业收入'], marker='o', label='营业收入')
    axes[0, 0].plot(profit['报告期'], profit['净利润'], marker='s', label='净利润')
    axes[0, 0].set_title('营收与利润趋势')
    axes[0, 0].legend()
    axes[0, 0].tick_params(axis='x', rotation=45)

    # 2. 盈利能力
    axes[0, 1].plot(indicator['报告期'], indicator['销售毛利率'], marker='o', label='毛利率')
    axes[0, 1].plot(indicator['报告期'], indicator['销售净利率'], marker='s', label='净利率')
    axes[0, 1].plot(indicator['报告期'], indicator['净资产收益率'], marker='^', label='ROE')
    axes[0, 1].set_title('盈利能力')
    axes[0, 1].legend()
    axes[0, 1].tick_params(axis='x', rotation=45)

    # 3. 成长性
    axes[1, 0].bar(indicator['报告期'], indicator['营业收入增长率'], alpha=0.7, label='营收增长')
    axes[1, 0].bar(indicator['报告期'], indicator['净利润增长率'], alpha=0.7, label='利润增长')
    axes[1, 0].set_title('成长性')
    axes[1, 0].legend()
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].axhline(0, color='black', linestyle='-', linewidth=0.5)

    # 4. 偿债能力
    axes[1, 1].plot(indicator['报告期'], indicator['流动比率'], marker='o', label='流动比率')
    axes[1, 1].plot(indicator['报告期'], indicator['资产负债率'], marker='s', label='资产负债率')
    axes[1, 1].set_title('偿债能力')
    axes[1, 1].legend()
    axes[1, 1].tick_params(axis='x', rotation=45)

    plt.suptitle(f'{name}({symbol}) 财务分析', fontsize=16)
    plt.tight_layout()
    plt.show()
```

## 5.7 财务选股器

```python
def stock_screener(criteria):
    """财务选股器"""

    # 获取股票列表
    stock_list = ak.stock_zh_a_spot_em()
    results = []

    for _, stock in stock_list.iterrows():
        symbol = stock['代码']
        name = stock['名称']

        try:
            # 获取财务数据
            _, _, _, indicator = get_financial_statements(symbol, name)
            latest = indicator.iloc[-1]

            # 应用筛选条件
            passed = True

            if 'min_roe' in criteria and latest['净资产收益率'] < criteria['min_roe']:
                passed = False

            if 'max_pe' in criteria:
                pe = stock['市盈率-动态']
                if pe == '-' or float(pe) > criteria['max_pe']:
                    passed = False

            if 'min_revenue_growth' in criteria:
                if latest['营业收入增长率'] < criteria['min_revenue_growth']:
                    passed = False

            if passed:
                results.append({
                    'code': symbol,
                    'name': name,
                    'roe': latest['净资产收益率'],
                    'revenue_growth': latest['营业收入增长率'],
                    'pe': stock['市盈率-动态'],
                    'price': stock['最新价']
                })

        except Exception as e:
            continue

    return pd.DataFrame(results)

# 使用示例
criteria = {
    'min_roe': 15,
    'max_pe': 30,
    'min_revenue_growth': 10
}
screener_results = stock_screener(criteria)
```

## 练习题

1. 计算贵州茅台近5年ROE平均值
2. 实现现金流结构分析
3. 编写杜邦分析函数
4. 比较同行业公司的财务指标

## 学习检查清单

- [ ] 能够获取并处理财务报表数据
- [ ] 掌握关键财务指标的计算
- [ ] 理解估值分析方法
- [ ] 能够进行财务异常检测
- [ ] 掌握财务数据可视化方法

## 下一步

财务分析掌握后 → [06-策略回测](../06-策略回测/)
