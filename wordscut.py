import jieba
import csv
import os
import re

# 配置路径
input_path = os.path.join('outputs', 'nameselect.txt')
output_path = os.path.join('outputs', 'cutwords.csv')

# 自定义否定词组（可根据需要扩展）
negation_phrases = [
    '不包邮', '不想玩', '不想用', '不退款', '不退', '不换',
    '不议价', '不打折', '不超过', '不支持', '不限制', '不能玩',
    '不需要', '不可以', '不接受', '不议价', '不议价', '不退换',
    '不含', '补邮费'
]

# 动态添加自定义词组
for phrase in negation_phrases:
    jieba.add_word(phrase, freq=1000)  # 设置高词频确保优先识别

# 读取数据
data = []
with open(input_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        # 分割编号和内容
        parts = line.split(':', 1)
        if len(parts) < 2:
            continue
        
        number, content = parts
        # 使用jieba分词
        words = jieba.lcut(content)
        # 过滤非有效字符（保留中文、字母、数字）
        filtered_words = [word for word in words if re.search(r'[\u4e00-\u9fa5a-zA-Z0-9]', word)]
        
        data.append((number, filtered_words))

# 写入CSV文件
with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    # # 写入表头（编号列+动态词语列）
    # writer.writerow(['编号', *['词语']*(max(len(words) for _, words in data))])
    
    for number, words in data:
        # 编号放在第一列，后面接所有词语
        writer.writerow([number] + words)