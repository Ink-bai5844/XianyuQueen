import jieba
import csv
import os
import re

input_path = os.path.join('outputs', 'nameselect.txt')
output_path = os.path.join('outputs', 'cutwords.csv')

# 自定义拆分屏蔽词组
negation_phrases = [
    '不包邮', '不想玩', '不想用', '不退款', '不退', '不换',
    '不议价', '不打折', '不超过', '不支持', '不限制', '不能玩',
    '不需要', '不可以', '不接受', '不议价', '不议价', '不退换',
    '不含', '补邮费'
]

# 动态添加
for phrase in negation_phrases:
    jieba.add_word(phrase, freq=1000)  # 高词频优先识别

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

        words = jieba.lcut(content)
        # 过滤非有效字符
        filtered_words = [word for word in words if re.search(r'[\u4e00-\u9fa5a-zA-Z0-9]', word)]
        
        data.append((number, filtered_words))

with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    # writer.writerow(['编号', *['词语']*(max(len(words) for _, words in data))])
    
    for number, words in data:
        writer.writerow([number] + words)