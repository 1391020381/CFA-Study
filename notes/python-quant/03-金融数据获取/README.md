# 03-金融数据获取

## 目标

掌握使用Python获取股票、财务、宏观经济等数据。

## 数据源对比

| 数据源 | 费用 | 数据范围 | 难度 | 推荐场景 |
|--------|------|----------|------|----------|
| AkShare | 免费 | A股全覆盖 | ⭐ | 新手首选 |
| Tushare | 积分制 | A股+港股 | ⭐⭐ | 数据质量要求高 |
| Baostock | 免费 | A股历史 | ⭐ | 历史回测 |
| yfinance | 免费 | 美股/港股 | ⭐⭐ | 美股投资 |
| 东方财富API | 爬虫 | 实时行情 | ⭐⭐⭐ | 实时监控 |

## 3.1 AkShare（推荐新手）

### 安装

```bash
pip install akshare
```

### 获取股票行情

```python
import akshare as ak

# 获取个股历史行情(前复权)
stock_data = ak.stock_zh_a_hist(
    symbol="000001",        # 股票代码
    period="daily",         # 日线数据
    start_date="20230101",  # 开始日期
    end_date="20231231",    # 结束日期
    adjust="qfq"            # 前复权
)

# 查看数据
print(stock_data.head())
```

### 获取财务数据

```python
# 获取资产负债表
balance_sheet = ak.stock_balance_sheet_by_report_em(symbol="贵州茅台")

# 获取利润表
income_statement = ak.stock_profit_sheet_by_report_em(symbol="贵州茅台")

# 获取现金流量表
cash_flow = ak.stock_cash_flow_sheet_by_report_em(symbol="贵州茅台")

# 获取财务指标
financial_indicator = ak.stock_financial_analysis_indicator(symbol="贵州茅台")
```

### 获取实时行情

```python
# 沪深京A股实时行情
stock_zh_a_spot = ak.stock_zh_a_spot_em()

# 筛选特定股票
stock_info = stock_zh_a_spot[stock_zh_a_spot['代码'] == '000001']
```

### 获取指数数据

```python
# 上证指数历史数据
sh_index = ak.stock_zh_index_daily(symbol="sh000001")

# 沪深300指数
hs300 = ak.stock_zh_index_daily(symbol="sh000300")
```

### 获取板块数据

```python
# 行业板块
sector = ak.stock_board_industry_name_em()

# 概念板块
concept = ak.stock_board_concept_name_em()

# 获取板块内个股
sector_stocks = ak.stock_board_industry_cons_em(symbol="白酒")
```

### 获取宏观数据

```python
# GDP数据
gdp = ak.macro_china_gdp()

# CPI数据
cpi = ak.macro_china_cpi()

# PMI数据
pmi = ak.macro_china_pmi()

# M2货币供应
m2 = ak.macro_china_m2()
```

## 3.2 Tushare

### 安装与注册

```bash
pip install tushare
```

需要注册获取token：https://tushare.pro/

### 基础使用

```python
import tushare as ts

# 设置token
ts.set_token('your_token_here')
pro = ts.pro_api()

# 获取股票列表
stock_list = pro.stock_basic(exchange='', list_status='L')

# 获取日线行情
df = pro.daily(
    ts_code='000001.SZ',
    start_date='20230101',
    end_date='20231231'
)

# 获取财务数据
# 利润表
income = pro.income(
    ts_code='000001.SZ',
    period='20231231',
    report_type='1'
)

# 资产负债表
balancesheet = pro.balancesheet(
    ts_code='000001.SZ',
    period='20231231'
)
```

## 3.3 数据存储

### 保存为CSV

```python
# 保存数据
stock_data.to_csv('stock_data.csv', index=False, encoding='utf-8-sig')

# 读取数据
df = pd.read_csv('stock_data.csv', parse_dates=['日期'])
df.set_index('日期', inplace=True)
```

### 保存到数据库

```python
import sqlite3

# 创建连接
conn = sqlite3.connect('stock_data.db')

# 保存
stock_data.to_sql('stock_000001', conn, if_exists='replace', index=False)

# 读取
df = pd.read_sql('SELECT * FROM stock_000001', conn)
```

### 增量更新

```python
def update_stock_data(symbol, conn):
    # 读取已有数据最新日期
    old_data = pd.read_sql(f'SELECT MAX(日期) as last_date FROM stock_{symbol}', conn)
    last_date = old_data['last_date'][0]

    # 获取新数据
    new_data = ak.stock_zh_a_hist(
        symbol=symbol,
        start_date=last_date,
        end_date=pd.Timestamp.now().strftime('%Y%m%d')
    )

    # 追加到数据库
    new_data.to_sql(f'stock_{symbol}', conn, if_exists='append', index=False)
```

## 3.4 数据清洗工具函数

```python
def standardize_stock_data(df):
    """标准化股票数据格式"""
    # 重命名列
    column_map = {
        '日期': 'date',
        '开盘': 'open',
        '收盘': 'close',
        '最高': 'high',
        '最低': 'low',
        '成交量': 'volume',
        '成交额': 'amount'
    }
    df = df.rename(columns=column_map)

    # 类型转换
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    # 确保数值类型
    numeric_cols = ['open', 'close', 'high', 'low', 'volume']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def check_data_quality(df):
    """检查数据质量"""
    print(f"数据行数: {len(df)}")
    print(f"缺失值:\n{df.isnull().sum()}")
    print(f"重复值: {df.duplicated().sum()}")
    print(f"数据范围: {df.index.min()} 至 {df.index.max()}")
    print(f"基本统计:\n{df.describe()}")
```

## 综合案例：构建股票数据库

```python
import akshare as ak
import pandas as pd
import sqlite3
from datetime import datetime

class StockDatabase:
    def __init__(self, db_path='stocks.db'):
        self.conn = sqlite3.connect(db_path)

    def get_stock_list(self):
        """获取所有A股列表"""
        stock_list = ak.stock_zh_a_spot_em()
        return stock_list[['代码', '名称', '最新价']]

    def download_stock_data(self, symbol, start_date='20200101'):
        """下载单只股票数据"""
        try:
            data = ak.stock_zh_a_hist(
                symbol=symbol,
                period='daily',
                start_date=start_date,
                adjust='qfq'
            )
            data['symbol'] = symbol
            return data
        except Exception as e:
            print(f"获取{symbol}数据失败: {e}")
            return None

    def save_to_db(self, data, table_name='stock_data'):
        """保存到数据库"""
        if data is not None:
            data.to_sql(table_name, self.conn, if_exists='append', index=False)

    def build_database(self, symbols=None, limit=None):
        """构建数据库"""
        if symbols is None:
            stock_list = self.get_stock_list()
            symbols = stock_list['代码'].tolist()

        if limit:
            symbols = symbols[:limit]

        for i, symbol in enumerate(symbols):
            print(f"进度: {i+1}/{len(symbols)} - {symbol}")
            data = self.download_stock_data(symbol)
            self.save_to_db(data)

    def read_stock(self, symbol):
        """读取股票数据"""
        query = f"SELECT * FROM stock_data WHERE symbol = '{symbol}' ORDER BY 日期"
        df = pd.read_sql(query, self.conn, parse_dates=['日期'])
        df.set_index('日期', inplace=True)
        return df

# 使用示例
db = StockDatabase('my_stocks.db')
# 测试下载几只股票
db.build_database(limit=10)
```

## 练习题

1. 下载贵州茅台最近3年数据并保存
2. 获取白酒板块所有股票的实时行情
3. 计算沪深300与中证500的相关性
4. 构建自己的股票数据库

## 学习检查清单

- [ ] 能够使用AkShare获取基本行情数据
- [ ] 掌握财务数据的获取方法
- [ ] 理解数据存储的各种方式
- [ ] 能够进行增量更新
- [ ] 掌握数据清洗的基本方法

## 下一步

数据获取掌握后 → [04-技术指标计算](../04-技术指标计算/) 或 [05-财务分析](../05-财务分析/)
