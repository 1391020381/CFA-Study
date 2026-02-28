# 08-进阶方向

## 目标

探索量化投资的进阶领域，选择适合的方向深入学习。

## 8.1 机器学习与量化

### 基础机器学习

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def ml_prediction_model(df):
    """使用机器学习预测股价涨跌"""

    # 准备特征
    features = [
        'MA5', 'MA20', 'RSI', 'MACD_DIF', 'Volume_Ratio',
        'returns', 'volatility'
    ]

    # 创建标签：次日涨跌
    df['target'] = (df['close'].shift(-1) > df['close']).astype(int)

    # 删除包含NaN的行
    df_ml = df[features + ['target']].dropna()

    X = df_ml[features]
    y = df_ml['target']

    # 划分训练测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, shuffle=False
    )

    # 训练模型
    model = RandomForestClassifier(n_estimators=100, max_depth=10)
    model.fit(X_train, y_train)

    # 预测
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # 特征重要性
    importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)

    return {
        'model': model,
        'accuracy': accuracy,
        'feature_importance': importance
    }
```

### XGBoost在量化中的应用

```python
import xgboost as xgb

def xgb_stock_prediction(df):
    """使用XGBoost预测"""

    # 特征工程
    def create_features(df):
        df['price_change'] = df['close'].pct_change()
        df['volume_change'] = df['volume'].pct_change()
        df['high_low_ratio'] = df['high'] / df['low']
        df['close_open_ratio'] = df['close'] / df['open']

        # 滞后特征
        for lag in [1, 2, 3, 5]:
            df[f'return_lag_{lag}'] = df['close'].pct_change(lag)

        return df

    df = create_features(df)

    # 选择特征列
    feature_cols = [col for col in df.columns if col not in ['target', 'date']]

    # XGBoost模型
    params = {
        'objective': 'binary:logistic',
        'max_depth': 6,
        'learning_rate': 0.1,
        'n_estimators': 100
    }

    model = xgb.XGBClassifier(**params)
    # ... 训练和预测代码
```

## 8.2 深度学习与量化

### LSTM时序预测

```python
import torch
import torch.nn as nn

class LSTMModel(nn.Module):
    """LSTM股价预测模型"""

    def __init__(self, input_size, hidden_size=64, num_layers=2):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.lstm = nn.LSTM(input_size, hidden_size, num_layers,
                           batch_first=True, dropout=0.2)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)

        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

def prepare_lstm_data(df, lookback=60):
    """准备LSTM训练数据"""
    # 数据标准化
    # 创建滑动窗口
    # 返回训练数据
    pass
```

### NLP分析研报

```python
from transformers import pipeline

def analyze_sentiment(text):
    """分析研报情感"""

    # 使用预训练模型
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="bert-base-chinese"
    )

    result = sentiment_pipeline(text)
    return result

def extract_keywords(text):
    """提取关键词"""
    import jieba
    import jieba.analyse

    keywords = jieba.analyse.extract_tags(text, topK=10)
    return keywords
```

## 8.3 期权与衍生品

### Black-Scholes期权定价

```python
import scipy.stats as stats

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    S: 标的资产价格
    K: 行权价
    T: 到期时间(年)
    r: 无风险利率
    sigma: 波动率
    option_type: 'call' 或 'put'
    """

    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    if option_type == 'call':
        price = S*stats.norm.cdf(d1) - K*np.exp(-r*T)*stats.norm.cdf(d2)
    else:
        price = K*np.exp(-r*T)*stats.norm.cdf(-d2) - S*stats.norm.cdf(-d1)

    # 计算希腊字母
    delta = stats.norm.cdf(d1) if option_type == 'call' else -stats.norm.cdf(-d1)
    gamma = stats.norm.pdf(d1) / (S*sigma*np.sqrt(T))
    vega = S*stats.norm.pdf(d1)*np.sqrt(T) / 100

    return {
        'price': price,
        'delta': delta,
        'gamma': gamma,
        'vega': vega
    }
```

### 波动率策略

```python
def calculate_historical_volatility(df, window=20):
    """计算历史波动率"""
    returns = df['close'].pct_change()
    volatility = returns.rolling(window).std() * np.sqrt(252)
    return volatility

def volatility_strategy(df, low_threshold=0.15, high_threshold=0.35):
    """波动率策略：低波动买入，高波动卖出"""
    df['volatility'] = calculate_historical_volatility(df)

    df['signal'] = 0
    df.loc[df['volatility'] < low_threshold, 'signal'] = 1
    df.loc[df['volatility'] > high_threshold, 'signal'] = -1

    return df
```

## 8.4 组合优化

### 马科维茨组合优化

```python
from scipy.optimize import minimize

def efficient_frontier(returns, num_portfolios=100):
    """计算有效前沿"""

    # 计算平均收益和协方差矩阵
    mean_returns = returns.mean()
    cov_matrix = returns.cov()

    results = []

    for _ in range(num_portfolios):
        # 随机权重
        weights = np.random.random(len(returns.columns))
        weights /= weights.sum()

        # 组合收益和风险
        portfolio_return = np.dot(weights, mean_returns) * 252
        portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)

        results.append({
            'return': portfolio_return,
            'risk': portfolio_std,
            'sharpe': portfolio_return / portfolio_std,
            'weights': weights
        })

    return pd.DataFrame(results)

def optimize_portfolio(returns, target_return=None):
    """优化投资组合"""

    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_assets = len(returns.columns)

    # 目标函数：最小化风险
    def portfolio_variance(weights):
        return np.dot(weights.T, np.dot(cov_matrix, weights))

    # 约束条件
    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]  # 权重和为1

    if target_return:
        constraints.append({
            'type': 'eq',
            'fun': lambda w: np.dot(w, mean_returns) * 252 - target_return
        })

    # 边界条件
    bounds = tuple((0, 1) for _ in range(num_assets))

    # 初始权重
    init_weights = num_assets * [1. / num_assets]

    # 优化
    result = minimize(
        portfolio_variance,
        init_weights,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    return result.x
```

### 风险平价策略

```python
def risk_parity(returns):
    """风险平价组合：各资产风险贡献相等"""

    cov_matrix = returns.cov()

    def risk_budget_objective(weights):
        # 组合波动率
        portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        # 边际风险贡献
        marginal_risk = np.dot(cov_matrix, weights) / portfolio_vol

        # 风险贡献
        risk_contributions = weights * marginal_risk

        # 目标：风险贡献相等
        target_contrib = np.ones(len(weights)) / len(weights)
        return np.sum((risk_contributions - target_contrib) ** 2)

    constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bounds = tuple((0, 1) for _ in range(len(returns.columns)))

    result = minimize(
        risk_budget_objective,
        x0=np.ones(len(returns.columns)) / len(returns.columns),
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )

    return result.x
```

## 8.5 高频交易

```python
class HighFrequencyStrategy:
    """简单高频策略框架"""

    def __init__(self, symbol):
        self.symbol = symbol
        self.order_book = {}  # 订单簿
        self.position = 0
        self.pnl = 0

    def update_order_book(self, bid_prices, ask_prices, bid_volumes, ask_volumes):
        """更新订单簿"""
        self.order_book = {
            'bid_prices': bid_prices,
            'ask_prices': ask_prices,
            'bid_volumes': bid_volumes,
            'ask_volumes': ask_volumes
        }

    def calculate_imbalance(self):
        """计算买卖失衡"""
        total_bid_volume = sum(self.order_book['bid_volumes'][:5])
        total_ask_volume = sum(self.order_book['ask_volumes'][:5])

        imbalance = (total_bid_volume - total_ask_volume) / (total_bid_volume + total_ask_volume)
        return imbalance

    def generate_signal(self):
        """生成交易信号"""
        imbalance = self.calculate_imbalance()

        if imbalance > 0.3:  # 买压大
            return 'BUY'
        elif imbalance < -0.3:  # 卖压大
            return 'SELL'
        else:
            return 'HOLD'
```

## 学习路径建议

根据兴趣选择方向：

| 方向 | 前置知识 | 学习周期 | 应用场景 |
|------|----------|----------|----------|
| 机器学习 | Python基础、统计学 | 2-3个月 | 因子挖掘、预测 |
| 深度学习 | ML基础、PyTorch | 3-6个月 | NLP、时序预测 |
| 期权定价 | 金融工程、微积分 | 2-3个月 | 波动率交易 |
| 组合优化 | 线性代数、优化理论 | 1-2个月 | 资产配置 |
| 高频交易 | 极低延迟系统 | 6个月+ | 机构交易 |

## 学习资源

### 机器学习
- scikit-learn文档
- 《量化投资：策略与技术》
- Kaggle竞赛

### 深度学习
- PyTorch官方教程
- Fast.ai课程
- 《深度学习》- Goodfellow

### 期权定价
- 《期权、期货及其他衍生产品》- Hull
- QuantLib库文档

### 组合优化
- cvxpy文档
- 《资产选择》- Markowitz

## 学习检查清单

- [ ] 确定感兴趣的方向
- [ ] 完成前置知识学习
- [ ] 实现基础算法
- [ ] 在回测中验证
- [ ] 持续学习新方法

---

恭喜你完成Python量化学习路径！持续学习和实践是进步的关键。
