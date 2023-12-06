import platform
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor

def contains_chinese_iterative(text):
  for char in text:
    if '\u4e00' <= char <= '\u9fa5':
        return True
  return False

def ping(host):
    system = platform.system()
    if system == "Windows":
        ping_cmd = ["ping", host, "-n", "4"]
    else:
        ping_cmd = ["ping", host, "-c", "4"]

    ping_process = subprocess.Popen(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, _ = ping_process.communicate()

    if system == "Windows":
        pattern = r"Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms"
        if contains_chinese_iterative(output):
          pattern = r"最短 = (\d+)ms，最长 = (\d+)ms，平均 = (\d+)ms"
        match = re.search(pattern, output)
        if match:
            return {
                "ip": host,
                "min": int(match.group(1)),
                "max": int(match.group(2)),
                "avg": int(match.group(3)),
                "packet_loss": 0
            }
    else:
        pattern = r"min/avg/max/mdev = (\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/\d+\.\d+ ms"
        if contains_chinese_iterative(output):
          pattern = r"最短/平均/最长/偏差 = (\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)/\d+\.\d+ ms"
        match = re.search(pattern, output)
        if match:
            return {
                "ip": host,
                "min": int(float(match.group(1))),
                "max": int(float(match.group(3))),
                "avg": int(float(match.group(2))),
                "packet_loss": 0
            }

        packet_loss_pattern = r"(\d+)% 丢失"
        packet_loss_match = re.search(packet_loss_pattern, output)
        if packet_loss_match:
            packet_loss = int(packet_loss_match.group(1))
            return {
                "ip": host,
                "min": 0,
                "max": 0,
                "avg": 0,
                "packet_loss": packet_loss
            }
    return None

# result = ping("www.baidu1.com")
# if result:
#     print("最小值:", result["min"])
#     print("最大值:", result["max"])
#     print("平均值:", result["avg"])
#     print("丢包率:", result["packet_loss"], "%")
# else:
#     print("无法获取ping结果")


def main():
    # 指定要ping的IP列表
    ip_list = ['114.114.114.114', '8.8.8.8', 'www.baidu.com']

    # 使用线程池执行ping操作
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(ping, ip_list))

    print(results)
    # 输出结果
    # for result in results:
    #     ip = result['ip']
    #     ping_result = result['result']
    #     if ping_result:
    #         print(f'IP地址: {ip}')
    #         if 'average_time' in ping_result:
    #             print(f'平均时间: {ping_result["average_time"]}ms')
    #             print(f'丢包率: {ping_result["packet_loss"]}%\n')
    #         else:
    #             print(f'最小时间: {ping_result["min_time"]}ms')
    #             print(f'平均时间: {ping_result["avg_time"]}ms')
    #             print(f'最大时间: {ping_result["max_time"]}ms')
    #             print(f'丢包率: {ping_result["packet_loss"]}%\n')
    #     else:
    #         print(f'无法获取 {ip} 的ping结果\n')

if __name__ == "__main__":
  main()