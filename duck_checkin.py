import requests
import datetime
import sys

# --- 配置区域 ---
url = "https://duckcoding.com/api/user/checkin"

# 根据你抓包的 cURL 提取的 Headers 
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-store",
    # 核心身份凭证，长期使用如果失效需更换这里的 session 值
    "cookie": "session=your session cookie",
    "new-api-user": "22792",  # 必须带上这个 ID
    "origin": "https://duckcoding.com",
    "referer": "https://duckcoding.com/console/personal",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}

def do_checkin():
    print(f"[{datetime.datetime.now()}] 开始执行签到...")
    try:
        # 发送 POST 请求
        response = requests.post(url, headers=headers)
        
        # 打印状态码和响应内容
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")

        # 简单判断逻辑 (假设200即为通信成功，具体成功与否看返回的JSON)
        if response.status_code == 200:
             # 如果返回 JSON，可以进一步解析，例如 response.json().get('msg')
            print(">> 请求发送成功 (请检查上方响应内容确认是否签到成功)")
        else:
            print(">> 请求失败")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    do_checkin()