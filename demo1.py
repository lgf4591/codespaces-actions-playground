import platform
import subprocess
import re

def contains_chinese_iterative(text):
  for char in text:
    if '\u4e00' <= char <= '\u9fa5':
        return True
  return False

def ping(host):
    system = platform.system()
    if system == "Windows":
        ping_cmd = ["ping", host, "-n", "4"]
        pattern = r"(Minimum = (\d+)ms|最短 = (\d+)ms), (Maximum = (\d+)ms|最长 = (\d+)ms), (Average = (\d+)ms|平均 = (\d+)ms)"
        packet_loss_pattern = r"(\d+)% loss|丢失 = (\d+)%"
    else:
        ping_cmd = ["ping", host, "-c", "4"]
        pattern = r"(\d+) bytes from .* time=(\d+\.\d+) ms"
        packet_loss_pattern = r"(\d+)% packet loss|(\d+)% 丢失"

    ping_process = subprocess.Popen(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, _ = ping_process.communicate()

    match = re.findall(pattern, output)
    packet_loss_match = re.search(packet_loss_pattern, output)

    if match:
        if system == "Windows":
            times = [int(x[5]) for x in match]
        else:
            times = [float(x[1]) for x in match]
        min_time = min(times)
        max_time = max(times)
        avg_time = sum(times) / len(times)
        packet_loss = int(packet_loss_match.group(1)) if packet_loss_match else 0
        return {
            "min": min_time,
            "max": max_time,
            "avg": avg_time,
            "packet_loss": packet_loss
        }
    return None

result = ping("www.baidu.com")
if result:
    print("最小值:", result["min"], "ms")
    print("最大值:", result["max"], "ms")
    print("平均值:", result["avg"], "ms")
    print("丢包率:", result["packet_loss"], "%")
else:
    print("无法获取ping结果")