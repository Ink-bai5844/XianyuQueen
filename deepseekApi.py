import csv
import json
import requests
import os
import time
import re

# 配置路径
gfc_path = os.path.join('Goofisher', 'src', 'gfc.json')
input_path = os.path.join('outputs', 'good.csv')
output_path = os.path.join('outputs', 'recommendation.csv')
nameselect_path = os.path.join('outputs', 'nameselect.txt')
price_path = os.path.join('outputs', 'price.txt')
result_path = os.path.join('outputs', 'result.csv')
log_path = os.path.join('outputs', 'api_debug.log')

# API配置（需替换实际参数）
API_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY = ""  # API密钥
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def log_debug_info(message):
    """记录调试信息"""
    with open(log_path, 'a', encoding='utf-8') as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")


def parse_api_response(content):
    """
    增强型API响应解析函数
    处理包含Markdown代码块、格式错误等情况
    """
    # 尝试提取代码块内容
    json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # 尝试直接解析整个内容
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    
    # 清理内容后尝试解析
    cleaned_content = content.replace('```', '').strip()
    try:
        return json.loads(cleaned_content)
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON format",
            "score": 0,
            "reasons": ["API返回数据解析失败"],
            "suggestion": "请联系技术支持",
            "raw_content": content[:200] + "..." if len(content) > 200 else content
        }

def validate_response(data):
    """验证并标准化响应数据结构"""
    if not isinstance(data, dict):
        data = {}
    
    return {
        "score": float(data.get("score", 0)),
        "reasons": data.get("reasons", ["数据解析异常"]),
        "suggestion": data.get("suggestion", "无"),
        "error": data.get("error", ""),
        "raw": data
    }

with open(gfc_path, 'r', encoding='utf-8') as f:
    gfc_data = json.load(f)

Productname = gfc_data["keyword"]

def analyze_text(text):
    """调用Deepseek API进行分析"""
    try:
        # 验证系统提示词文件
        if not os.path.exists('system_prompt.txt'):
            raise FileNotFoundError("系统提示词文件缺失")
            
        system_prompt = open('system_prompt.txt', 'r', encoding='utf-8').read()
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"我要买的是：{Productname}\n请分析以下商品信息：\n{text}"} #加入商品判断，避免断货现象
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        # 添加超时和重试机制
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    API_URL,
                    headers=HEADERS,
                    json=payload,
                    timeout=(3.05, 27)
                )
                
                # 记录原始响应
                log_debug_info(f"API响应原始数据：{response.text}")
                
                if response.status_code != 200:
                    raise requests.exceptions.HTTPError(
                        f"HTTP错误 {response.status_code}"
                    )
                
                response_data = response.json()
                
                # 验证响应结构
                if 'choices' not in response_data:
                    raise ValueError("无效API响应结构")
                
                # 修改后的解析逻辑
                content = response_data['choices'][0]['message']['content']
                parsed_data = parse_api_response(content)
                validated_data = validate_response(parsed_data)
                
                return validated_data
                
            except (requests.Timeout, requests.ConnectionError) as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    log_debug_info(f"超时重试中（第{attempt+1}次）等待{wait_time}秒...")
                    time.sleep(wait_time)
                    continue
                else:
                    raise
                    
    except Exception as e:
        log_debug_info(f"API调用失败：{str(e)}")
        return {
            "error": str(e),
            "score": 0,
            "reasons": ["API服务不可用"],
            "suggestion": "请检查网络连接和API配置"
        }

# 读取数据并分析
results = []
with open(input_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        log_debug_info(f"开始处理编号 {row['编号']}")
        
        # 构建分析文本
        input_text = f"""
        【商品描述】{row['介绍']}
        【价格信息】{row.get('价格', '未提供')}
        """
        
        # 执行分析
        analysis = analyze_text(input_text)
        
        # 记录详细结果
        log_debug_info(f"编号{row['编号']}分析结果：{json.dumps(analysis, ensure_ascii=False)}")
        
        results.append({
            '编号': row['编号'],
            '评分': analysis.get('score', 0),
            '分析结果': analysis
        })

# 排序并保存结果
sorted_results = sorted(
    results, 
    key=lambda x: x['评分'], 
    reverse=True
)[:10]

with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['排名', '编号', '推荐指数', '核心亮点', '详细分析'])
    for idx, item in enumerate(sorted_results, 1):
        analysis = item['分析结果']
        highlights = analysis.get('reasons', [])[:2]
        writer.writerow([
            idx,
            item['编号'],
            analysis.get('score', 0),
            "；".join(highlights),
            json.dumps(analysis, ensure_ascii=False)
        ])

print(f"分析完成，调试日志已保存至：{log_path}")
print(f"推荐结果保存至：{output_path}")

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

with open(result_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['编号', '推荐指数', '价格', '介绍'])
    for item in sorted_results:
        number = item['编号']
        if number in descriptions and number in prices:
            writer.writerow([
                number,
                item['分析结果'].get('score', 0),
                prices[number],
                descriptions[number]
            ])
        else:
            print(f"警告：编号{number}缺少对应介绍或价格")
            continue

print(f"最终结果保存至：{result_path}")
print("所有操作完成。")