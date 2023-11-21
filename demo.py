import subprocess
import re
import platform
import locale

def run_ping(host, count=4):
    # 根据操作系统选择合适的ping命令
    system = platform.system()
    if system == 'Windows':
        command = ['ping', '-n', str(count), host]
    else:
        # 默认使用Unix风格的ping命令（适用于Linux和MacOS）
        command = ['ping', '-c', str(count), host]

    try:
        # 运行ping命令
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)

        # 检查是否成功运行ping命令
        if result.returncode == 0:
            return result.stdout
        else:
            return None
    except subprocess.TimeoutExpired:
        return None

def parse_ping_output(output):
    # 获取系统语言
    sys_language, _ = locale.getlocale()

    # 根据操作系统和语言选择合适的正则表达式
    system = platform.system()
    if system == 'Windows':
        if 'chinese' in sys_language.lower():
            # Windows中文系统的正则表达式
            match = re.search(r'平均 = (\d+)ms.*?(\d+)% 丢失', output, re.DOTALL)
        else:
            # Windows英文系统的正则表达式
            match = re.search(r'Average = (\d+)ms.*?(\d+)% loss', output, re.DOTALL)
    else:
        if 'chinese' in sys_language.lower():
            # Unix中文系统的正则表达式
            match = re.search(r'(\d+)/(\d+)/(\d+)/(\d+\.\d+)% 丢包', output, re.DOTALL)
        else:
            # Unix英文系统的正则表达式
            match = re.search(r'(\d+)/(\d+)/(\d+)/(\d+\.\d+)% packet loss', output, re.DOTALL)

    print(match)
    if match:
        if system == 'Windows':
            average_time = int(match.group(1))
            packet_loss = int(match.group(2))
            return {'average_time': average_time, 'packet_loss': packet_loss}
        else:
            # Unix风格的ping输出包含最小、平均、最大三个时间值
            min_time, avg_time, max_time, packet_loss = map(float, match.groups())
            return {'min_time': min_time, 'avg_time': avg_time, 'max_time': max_time, 'packet_loss': packet_loss}
    else:
        return None

# 指定要ping的主机
host_to_ping = 'baidu.com'

# 运行ping命令并获取输出
ping_output = run_ping(host_to_ping)
print(ping_output)

if ping_output:
    # 解析ping输出并获取各项指标
    result = parse_ping_output(ping_output)
    if result:
        if 'average_time' in result:
            print(f'平均时间: {result["average_time"]}ms')
            print(f'丢包率: {result["packet_loss"]}%')
        else:
            print(f'最小时间: {result["min_time"]}ms')
            print(f'平均时间: {result["avg_time"]}ms')
            print(f'最大时间: {result["max_time"]}ms')
            print(f'丢包率: {result["packet_loss"]}%')
    else:
        print('无法解析ping输出')
else:
    print('无法执行ping命令')
