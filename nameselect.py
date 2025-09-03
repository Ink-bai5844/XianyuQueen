import csv
import os

# 配置路径
price_path = os.path.join('outputs', 'priceselect.csv')
name_path = os.path.join('outputs', 'name.txt')
output_path = os.path.join('outputs', 'nameselect.txt')

# 读取筛选后的编号集合
selected_numbers = set()
with open(price_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if row:  # 跳过空行
            selected_numbers.add(row[0])  # 读取第一列编号

# 读取name.txt并筛选对应行
matched_lines = []
with open(name_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        # 分割编号和内容
        parts = line.split(':', 1)
        if len(parts) < 2:
            continue
        
        number = parts[0]
        if number in selected_numbers:
            matched_lines.append(line)  # 保留原始格式

# 保存结果
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(matched_lines))

print(f"已匹配{len(matched_lines)}条数据保存至：{output_path}")