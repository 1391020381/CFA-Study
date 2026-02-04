import akshare as ak
import sys
import io

# Set stdout to UTF-8 encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

stock_sse_summary_df = ak.stock_sse_summary()
print(stock_sse_summary_df)
