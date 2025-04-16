# XianyuQueen - 基于价格筛查、词向量关联及deepseek深度分析的闲鱼商品智能分析推荐系统

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
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
```bash
API_KEY = "sk-XXXXX"  # API密钥
```

4. 配置偏好向量字符串(gfc.json)[其他配置请见https://github.com/MiankeStar/Goofisher]
```json
"wordscut": "现货包邮正品RTX显卡未拆全新"
```

## 🎮 使用方法
完整流程运行
```bash
python run.py
```

或分步执行
```bash
# 1. 数据采集
python Goofisher/src/process/gfcp.py

# 2. 价格筛选
python priceselect.py

# 3. 名称匹配
python nameselect.py

# 4. 文本分析
python wordscut.py

# 5. 深度分析
python deepseekApi.py
```

## 📊 示例输出
推荐结果示例(result.csv)
```bash
编号,推荐指数,价格,介绍
43,9.0,10000.0,全新9999G显卡  
104,9.0,11000.0,显卡现货全新未拆
25,9.0,9999.0,全新未拆封显卡，32GB显存
```

深度分析实时日志(api_debug.log)
```bash
[2025-04-16 18:56:10] 开始处理编号 25
[2025-04-16 18:56:18] API响应原始数据：{"..."}
[2025-04-16 18:56:18] 编号25分析结果：{"..."}
```

## ⚠️ 注意事项
1. 首次使用需配置Chrome浏览器路径
2. 深度分析API出现网络错误时自动重试3次

## 🙏 致谢

本项目的开发基于以下开源项目：

- **[Goofisher](https://github.com/MiankeStar/Goofisher)**  
  由 MiankeStar 维护的闲鱼数据采集框架，为系统提供核心数据抓取能力
