# 00-环境准备

## 目标

搭建完整的Python量化开发环境。

## 安装步骤

### 1. 安装Anaconda（推荐）

**下载地址：** https://www.anaconda.com/

选择Python 3.10或3.11版本。

### 2. 创建专用环境

```bash
# 创建量化环境
conda create -n quant python=3.10

# 激活环境
conda activate quant
```

### 3. 安装核心库

```bash
# 数据处理
pip install numpy pandas

# 绘图
pip install matplotlib seaborn plotly

# 金融数据
pip install akshare tushare baostock yfinance

# 回测框架
pip install backtrader

# 技术分析
pip install ta-lib ta

# Jupyter
pip install jupyter jupyterlab
```

### 4. 安装Jupyter扩展

```bash
# 代码补全
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install

# 变量检查器
jupyter nbextension enable varInspector/main
```

### 5. IDE选择

| 工具 | 优点 | 适用场景 |
|------|------|----------|
| Jupyter Lab | 交互式、可视化 | 学习、数据分析 |
| VSCode | 轻量、插件丰富 | 日常开发 |
| PyCharm | 功能强大 | 大型项目 |

## 验证安装

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import akshare as ak

print("环境配置成功！")
print(f"NumPy: {np.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"AkShare: {ak.__version__}")
```

## 常见问题

### TA-Lib安装失败

**Windows方案：** 下载预编译wheel文件

```bash
# 访问 https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
# 下载对应版本的whl文件后安装
pip install TA_Lib-0.4.XX-cpXXX-cpXXX-win_amd64.whl
```

### 国内镜像加速

```bash
# pip配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# conda配置
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
```

## 下一步

环境配置完成后 → [01-Python基础](../01-Python基础/)
