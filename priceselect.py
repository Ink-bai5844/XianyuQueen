import numpy as np
import csv
import os

# 配置路径
input_path = os.path.join('outputs', 'price.txt')
output_path = os.path.join('outputs', 'priceselect.csv')

# 读取数据
data = []
with open(input_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        # 分割编号和价格
        parts = line.split(':', 1)
        if len(parts) != 2:
            continue
        
        try:
            number, price = parts[0], float(parts[1])
            data.append((number, price))
        except ValueError:
            continue

# 计算价格分布
prices = [item[1] for item in data]
q1 = np.percentile(prices, 25)
q3 = np.percentile(prices, 75)
iqr = q3 - q1

# 计算正常价格范围
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

# 筛选正常价格数据
normal_prices = [item for item in data if lower_bound <= item[1] <= upper_bound]

# 动态调整结果数量（最多100条）
selected = normal_prices[:100]

# 计算极值
min_price = min(item[1] for item in selected) if selected else None
max_price = max(item[1] for item in selected) if selected else None

# 保存结果
with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['编号', '价格'])
    for item in selected:
        writer.writerow(item)

# 输出结果
print(f"正常价格最小值: {min_price}")
print(f"正常价格最大值: {max_price}")
print(f"已筛选出{len(selected)}条数据保存至：{output_path}")