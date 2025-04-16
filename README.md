# XianyuQueen - 基于价格筛查、词向量关联及deepseek深度分析的闲鱼商品智能分析推荐系统

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 项目简介

本系统是针对闲鱼平台商品交易的智能分析工具，通过多阶段数据处理流水线，实现从商品数据采集到深度语义分析的完整流程。核心功能包括价格分布建模、关键词匹配、文本特征提取和AI推荐分析。

## 🚀 功能特性

- **自动化数据采集**：模拟浏览器获取商品列表
- **智能价格筛选**：基于IQR方法的异常值检测
- **多维度分析**：
  - 商品描述文本分词处理
  - 关键词向量化建模
  - DeepSeek大模型关联度分析
- **可视化输出**：生成CSV格式的推荐清单

## 📂 项目结构
```bash
XianyuQueen/
├── Goofisher/
│ └── src/
│  └── process/
│   └── gfcp.py # 数据采集主程序
│  └── gfc.json # 配置文件
├── outputs/
│ ├── name.txt  # 原始介绍数据
│ ├── price.txt # 原始价格数据
│ ├── priceselect.csv # 筛选后价格数据
│ ├── good.csv # 词向量匹配后商品数据
│ ├── recommendation.csv # 推荐原始数据
│ └── result.csv # 最终推荐结果
└── run.py # 流水线控制
```

## 🛠️ 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourname/XianyuQueen.git
cd XianyuQueen
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 申请DeepSeek API密钥并配置(deepseekApi.py)
```json
{
    "browser_path": "C:/Program Files/Google/Chrome/Application/chrome.exe",
    "wordscut": "包邮,国行,港版,二手,正版,中文,现货",
    "api_key": "your_deepseek_api_key"
}
```