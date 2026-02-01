#!/usr/bin/env python3
"""
招商银行市盈率趋势分析
获取近10年数据，计算PE及统计指标
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# 招商银行A股代码
STOCK_CODE = "600036"
YEARS = 10

def get_stock_price():
    """获取招商银行历史股价数据"""
    print("正在获取历史股价数据...")
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=YEARS*365)).strftime("%Y%m%d")

    # 使用akshare获取股票历史数据
    try:
        stock_df = ak.stock_zh_a_hist(symbol=STOCK_CODE, period="daily",
                                      start_date=start_date, end_date=end_date,
                                      adjust="")  # 不复权
        stock_df['日期'] = pd.to_datetime(stock_df['日期'])
        return stock_df[['日期', '收盘', '开盘', '最高', '最低', '成交量']]
    except Exception as e:
        print(f"获取股价数据失败: {e}")
        return None

def get_eps_data():
    """获取招商银行EPS数据（加权每股收益，季度累计）"""
    print("正在获取EPS数据...")

    try:
        # 使用akshare获取个股财务指标
        financial_df = ak.stock_financial_analysis_indicator(symbol=STOCK_CODE)

        # 转换日期格式
        financial_df['日期'] = pd.to_datetime(financial_df['日期'])

        # 筛选近10年数据（多取一些以确保有足够数据计算TTM）
        financial_df = financial_df[financial_df['日期'] >= (datetime.now() - timedelta(days=YEARS*365 + 365))]

        # 使用摊薄每股收益（同花顺使用的标准）
        eps_col = '摊薄每股收益(元)'
        if eps_col not in financial_df.columns:
            print(f"未找到 {eps_col}，可用的列:", [c for c in financial_df.columns if '每股收益' in c])
            return None

        result = financial_df[['日期', eps_col]].copy()
        result.rename(columns={eps_col: 'EPS累计'}, inplace=True)

        # 按日期排序
        result = result.sort_values('日期').reset_index(drop=True)

        # 计算单季度EPS
        # Q1(03月): 直接使用累计值
        # Q2(06月): Q2累计 - Q1累计
        # Q3(09月): Q3累计 - Q2累计
        # Q4(12月): Q4累计 - Q3累计
        result['季度'] = result['日期'].dt.month.map({3: 'Q1', 6: 'Q2', 9: 'Q3', 12: 'Q4'})
        result['年份'] = result['日期'].dt.year

        quarterly_eps = []
        for i in range(len(result)):
            curr_quarter = result.iloc[i]['季度']
            curr_cumulative = result.iloc[i]['EPS累计']

            if curr_quarter == 'Q1':
                # Q1直接使用累计值
                quarterly_eps.append(curr_cumulative)
            else:
                # 找到同一年上一个季度的累计值
                prev_quarter_map = {'Q2': 'Q1', 'Q3': 'Q2', 'Q4': 'Q3'}
                prev_quarter = prev_quarter_map[curr_quarter]
                curr_year = result.iloc[i]['年份']

                prev_row = result[(result['年份'] == curr_year) & (result['季度'] == prev_quarter)]

                if len(prev_row) > 0:
                    prev_cumulative = prev_row.iloc[0]['EPS累计']
                    quarterly_eps.append(curr_cumulative - prev_cumulative)
                else:
                    # 找不到上一季度，用累计值
                    quarterly_eps.append(curr_cumulative)

        result['EPS'] = quarterly_eps

        print(f"获取到 {len(result)} 条EPS数据")
        print(f"单季度EPS范围: {result['EPS'].min():.2f} - {result['EPS'].max():.2f}")

        return result

    except Exception as e:
        print(f"获取EPS数据失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def calculate_ttm_eps(trade_date, eps_df):
    """计算指定日期的TTM EPS（最近4个季度EPS之和）"""
    # 获取该日期之前（含）的所有EPS数据
    past_eps = eps_df[eps_df['日期'] <= trade_date].copy()

    if len(past_eps) < 4:
        return None

    # 取最近4个季度的EPS
    recent_4 = past_eps.tail(4)
    ttm_eps = recent_4['EPS'].sum()

    return ttm_eps

def calculate_pe_ratio(stock_df, eps_df):
    """计算市盈率时间序列（使用TTM EPS）"""
    print("正在计算TTM市盈率...")

    # 确保日期列是datetime类型
    stock_df['日期'] = pd.to_datetime(stock_df['日期'])
    eps_df['日期'] = pd.to_datetime(eps_df['日期'])

    # 按日期排序
    eps_df = eps_df.sort_values('日期')
    stock_df = stock_df.sort_values('日期').copy()

    # 为每个交易日计算TTM EPS
    print("正在计算TTM EPS...")
    ttm_eps_list = []
    for trade_date in stock_df['日期']:
        ttm_eps = calculate_ttm_eps(trade_date, eps_df)
        ttm_eps_list.append(ttm_eps)

    stock_df['EPS_TTM'] = ttm_eps_list

    # 计算PE = 收盘价 / TTM EPS
    stock_df['PE'] = stock_df['收盘'] / stock_df['EPS_TTM']

    # 删除EPS_TTM为空的行
    stock_df = stock_df.dropna(subset=['PE', 'EPS_TTM'])

    # 将EPS_TTM重命名为EPS用于输出
    stock_df = stock_df.rename(columns={'EPS_TTM': 'EPS'})

    return stock_df

def calculate_statistics(df):
    """计算统计指标"""
    print("正在计算统计指标...")

    pe_values = df['PE'].dropna()

    stats = {
        'mean': float(pe_values.mean()),
        'median': float(pe_values.median()),
        'std': float(pe_values.std()),
        'min': float(pe_values.min()),
        'max': float(pe_values.max()),
        'low_value_zone': float(pe_values.mean() - pe_values.std()),  # 均值 - 1个标准差
        'high_value_zone': float(pe_values.mean() + pe_values.std()),  # 均值 + 1个标准差
        'extreme_low': float(pe_values.mean() - 2 * pe_values.std()),  # 均值 - 2个标准差
        'extreme_high': float(pe_values.mean() + 2 * pe_values.std()),  # 均值 + 2个标准差
    }

    # 百分位数
    for p in [10, 25, 50, 75, 90]:
        stats[f'p{p}'] = float(pe_values.quantile(p/100))

    return stats

def main():
    print(f"开始获取招商银行({STOCK_CODE})近{YEARS}年数据...")

    # 1. 获取股价数据
    stock_df = get_stock_price()
    if stock_df is None:
        return

    print(f"股价数据: {len(stock_df)} 条记录")
    print(f"日期范围: {stock_df['日期'].min()} 至 {stock_df['日期'].max()}")

    # 2. 获取EPS数据
    eps_df = get_eps_data()
    if eps_df is None:
        print("无法获取EPS数据，尝试替代方案...")
        return

    print(f"EPS数据: {len(eps_df)} 条记录")
    print(f"EPS范围: {eps_df['EPS'].min():.2f} - {eps_df['EPS'].max():.2f}")

    # 3. 计算PE
    result_df = calculate_pe_ratio(stock_df, eps_df)

    # 4. 计算统计指标
    stats = calculate_statistics(result_df)

    # 5. 保存数据
    output_data = {
        'stock_code': STOCK_CODE,
        'stock_name': '招商银行',
        'data_period': f'{YEARS}年',
        'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'statistics': stats,
        'data': result_df.to_dict('records')
    }

    # 保存为JSON
    output_file = '/Users/zhoujin/Desktop/web/CFP-Study/notes/cmb_pe_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, default=str)

    print(f"\n数据已保存到: {output_file}")
    print(f"\n统计指标:")
    print(f"  PE均值: {stats['mean']:.2f}")
    print(f"  PE标准差: {stats['std']:.2f}")
    print(f"  低估值区间 (均值-1标准差): {stats['low_value_zone']:.2f}")
    print(f"  高估值区间 (均值+1标准差): {stats['high_value_zone']:.2f}")
    print(f"  PE最小值: {stats['min']:.2f}")
    print(f"  PE最大值: {stats['max']:.2f}")

if __name__ == "__main__":
    main()
