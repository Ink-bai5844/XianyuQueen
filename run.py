import os
import subprocess
import sys
from time import perf_counter

# 流水线配置
PIPELINE = [
    {
        "name": "数据采集",
        "path": os.path.join("Goofisher", "src", "process", "gfcp.py"),
        "timeout": 300000  # 修正为合理值（300秒）
    },
    {
        "name": "价格筛选",
        "path": "priceselect.py",
        "depends": [os.path.join("outputs", "price.txt")]
    },
    {
        "name": "名称匹配",
        "path": "nameselect.py",
        "depends": [os.path.join("outputs", "priceselect.csv")]
    },
    {
        "name": "文本分词",
        "path": "wordscut.py",
        "depends": [os.path.join("outputs", "nameselect.txt")]
    },
    {
        "name": "词向量分析",
        "path": "wordVectors.py",
        "depends": [os.path.join("outputs", "cutwords.csv")]
    },
    {
        "name": "深度分析",
        "path": "deepseekApi.py",
        "depends": [os.path.join("outputs", "good.csv")]
    }
]

def validate_dependencies(depends):
    """验证前置文件是否存在"""
    missing = []
    for file in depends:
        if not os.path.exists(file):
            missing.append(file)
    return missing

def run_step(step, index):
    """执行单个步骤（带实时输出）"""
    print(f"\n{'='*40}")
    print(f"步骤 {index+1}/{len(PIPELINE)} | {step['name']}")
    print(f"执行脚本: {step['path']}")
    
    # 检查前置文件
    if 'depends' in step:
        missing_files = validate_dependencies(step['depends'])
        if missing_files:
            print(f"错误：缺少前置文件:")
            for f in missing_files:
                print(f"  - {f}")
            return False
    
    # 执行命令
    cmd = [sys.executable, step['path']]
    start_time = perf_counter()
    
    try:
        # 启动子进程
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # 行缓冲
            universal_newlines=True
        )
        
        # 实时读取输出
        while True:
            # 检查超时
            elapsed = perf_counter() - start_time
            if elapsed > step.get('timeout', 6000):
                process.terminate()
                raise subprocess.TimeoutExpired(cmd, step['timeout'])
            
            # 读取输出
            output = process.stdout.readline()
            if output:
                print(f"[{step['name']}] {output.strip()}")
                
            # 检查进程状态
            if process.poll() is not None:
                break
                
            # # 避免CPU占用过高
            # time.sleep(0.1)
        
        # 获取剩余输出
        remaining_output, _ = process.communicate()
        if remaining_output:
            print(remaining_output.strip())
        
        # 检查返回码
        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode, 
                cmd, 
                output=remaining_output
            )
            
        print(f"[成功] 总耗时 {perf_counter() - start_time:.1f}s")
        return True
        
    except subprocess.TimeoutExpired:
        print(f"\n错误：执行超时（超过{step['timeout']}秒）")
        return False
    except subprocess.CalledProcessError as e:
        print(f"\n错误：退出码 {e.returncode}")
        if e.output:
            print("最后输出:\n" + e.output[:1000])
        return False

def main():
    print(f"=== 开始执行数据分析流水线 ===")
    print(f"Python版本: {sys.version.split()[0]}")
    print(f"工作目录: {os.getcwd()}")
    
    for idx, step in enumerate(PIPELINE):
        success = run_step(step, idx)
        if not success:
            print("\n!! 流水线执行失败 !!")
            sys.exit(1)
    
    print("\n=== 所有步骤执行完成 ===")
    final_output = os.path.join("outputs", "recommendation.csv")
    if os.path.exists(final_output):
        print(f"最终结果文件: {final_output}")

if __name__ == "__main__":
    main()