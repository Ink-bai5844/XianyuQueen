import json
import csv
import os
import re
import jieba

cutwords_path = os.path.join('outputs', 'cutwords.csv')
gfc_path = os.path.join('Goofisher', 'src', 'gfc.json')
nameselect_path = os.path.join('outputs', 'nameselect.txt')
price_path = os.path.join('outputs', 'price.txt')
output_path = os.path.join('outputs', 'good.csv')

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

with open(gfc_path, 'r', encoding='utf-8') as f:
    gfc_data = json.load(f)

    sentence = gfc_data["wordscut"]

    words = jieba.lcut(sentence)
    
    keywords = set()
    for word in words:
        cleaned_word = word.strip().lower()
        # 过滤非有效字符
        if re.search(r'[\u4e00-\u9fa5a-zA-Z0-9]', cleaned_word):
            keywords.add(cleaned_word)

print(f"关键词分词完成，共{len(keywords)}个关键词。")
for keyword in keywords:
    print(keyword)

# 构建编号-词组字典
word_vectors = {}
with open(cutwords_path, 'r', encoding='utf-8-sig') as f:  # 修改编码为utf-8-sig
    reader = csv.reader(f)
    for row in reader:
        if not row:
            continue
        # 清理编号并验证有效性
        number = row[0].strip()
        if not number.isdigit():
            print(f"跳过无效编号：{number}")
            continue
        words = [w.strip().lower() for w in row[1:]]
        word_vectors[number] = words

# 计算关联度得分
scores = []
for number, words in word_vectors.items():
    score = sum(1 for word in words if word in keywords)
    scores.append((number, score))

# 按得分排序
sorted_items = sorted(scores, key=lambda x: (-x[1], int(x[0])))[:10]

# 读取商品介绍
descriptions = {}
with open(nameselect_path, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split(':', 1)
        if len(parts) == 2:
            descriptions[parts[0]] = parts[1]

# 读取价格数据
prices = {}
with open(price_path, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split(':', 1)
        if len(parts) == 2:
            prices[parts[0]] = parts[1]

with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['编号', '介绍', '价格'])
    
    # for number, _ in sorted_items:
    #     if number in descriptions:
    #         writer.writerow([number, descriptions[number]])
    #     else:
    #         print(f"警告：编号{number}缺少对应介绍")
    for number, _ in sorted_items:
        if number in descriptions and number in prices:
            writer.writerow([number, descriptions[number], "价格：" + prices[number]])
        else:
            print(f"警告：编号{number}缺少对应介绍或价格")

print(f"关联分析完成，结果已保存至：{output_path}")