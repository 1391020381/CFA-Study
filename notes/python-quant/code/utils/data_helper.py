"""
数据获取与处理工具函数
"""

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta


def get_stock_data(symbol, start_date=None, end_date=None, adjust='qfq'):
    """
    获取股票历史数据

    Parameters:
    -----------
    symbol : str
        股票代码，如 '000001'
    start_date : str
        开始日期，格式 'YYYYMMDD'
    end_date : str
        结束日期，格式 'YYYYMMDD'
    adjust : str
        复权方式: 'qfq'-前复权, 'hfq'-后复权, ''-不复权

    Returns:
    --------
    DataFrame : 包含OHLCV数据
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y%m%d')

    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365*3)).strftime('%Y%m%d')

    try:
        data = ak.stock_zh_a_hist(
            symbol=symbol,
            period="daily",
            start_date=start_date,
            end_date=end_date,
            adjust=adjust
        )

        if data.empty:
            print(f"警告: 股票 {symbol} 没有数据")
            return None

        # 标准化列名
        column_map = {
            '日期': 'date',
            '开盘': 'open',
            '收盘': 'close',
            '最高': 'high',
            '最低': 'low',
            '成交量': 'volume',
            '成交额': 'amount'
        }
        data = data.rename(columns=column_map)

        # 设置日期索引
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)

        # 确保数值类型
        numeric_cols = ['open', 'close', 'high', 'low', 'volume']
        for col in numeric_cols:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')

        return data

    except Exception as e:
        print(f"获取股票 {symbol} 数据失败: {e}")
        return None


def get_stock_list():
    """
    获取所有A股列表

    Returns:
    --------
    DataFrame : 股票列表
    """
    try:
        stock_list = ak.stock_zh_a_spot_em()
        return stock_list
    except Exception as e:
        print(f"获取股票列表失败: {e}")
        return pd.DataFrame()


def save_to_csv(data, filename):
    """
    保存数据到CSV文件

    Parameters:
    -----------
    data : DataFrame
        要保存的数据
    filename : str
        文件名
    """
    try:
        data.to_csv(filename, encoding='utf-8-sig')
        print(f"数据已保存到 {filename}")
    except Exception as e:
        print(f"保存数据失败: {e}")


def load_from_csv(filename, parse_dates=True):
    """
    从CSV文件加载数据

    Parameters:
    -----------
    filename : str
        文件名
    parse_dates : bool
        是否解析日期

    Returns:
    --------
    DataFrame : 加载的数据
    """
    try:
        if parse_dates:
            data = pd.read_csv(filename, parse_dates=['date'], index_col='date')
        else:
            data = pd.read_csv(filename)
        print(f"数据已从 {filename} 加载")
        return data
    except Exception as e:
        print(f"加载数据失败: {e}")
        return None


def resample_data(data, freq='M'):
    """
    重采样数据

    Parameters:
    -----------
    data : DataFrame
        原始数据
    freq : str
        重采样频率: 'D'-日, 'W'-周, 'M'-月, 'Q'-季度

    Returns:
    --------
    DataFrame : 重采样后的数据
    """
    resampled = data.resample(freq).agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).dropna()

    return resampled


def calculate_returns(data, method='simple'):
    """
    计算收益率

    Parameters:
    -----------
    data : Series or DataFrame
        价格数据
    method : str
        'simple': 简单收益率, 'log': 对数收益率

    Returns:
    --------
    Series or DataFrame : 收益率
    """
    if method == 'simple':
        return data.pct_change()
    elif method == 'log':
        return np.log(data / data.shift(1))
    else:
        raise ValueError("method必须是'simple'或'log'")


if __name__ == "__main__":
    # 测试代码
    print("测试数据获取功能...")

    # 获取股票数据
    data = get_stock_data("000001")
    if data is not None:
        print(f"\n获取数据成功，共 {len(data)} 条记录")
        print(data.head())

        # 计算收益率
        data['returns'] = calculate_returns(data['close'])
        print("\n收益率统计:")
        print(data['returns'].describe())
