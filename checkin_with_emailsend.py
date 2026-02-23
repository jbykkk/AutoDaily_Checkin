import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import datetime
import traceback
import sys

# ============== 配置区 ==============
# SMTP 邮件告警
SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER_EMAIL = "your_account@163.com"      # 替换为你的网易邮箱
AUTH_CODE = "YOUR_163_AUTH_CODE"           # 替换为 SMTP 授权码
RECEIVER_EMAIL = "your_account@qq.com"     # 替换为接收告警的邮箱

# Duckcoding 签到配置
CHECKIN_URL = "https://duckcoding.com/api/user/checkin"
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-store",
    "cookie": "session=your_session_cookie",  # 替换为你的 session cookie
    "new-api-user": "22792",
    "origin": "https://duckcoding.com",
    "referer": "https://duckcoding.com/console/personal",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
}
# ====================================

def send_alert_email(subject, content):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = formataddr((Header("签到监控服务", 'utf-8').encode(), SENDER_EMAIL))
    message['To'] = formataddr((Header("监控终端", 'utf-8').encode(), RECEIVER_EMAIL))
    message['Subject'] = Header(subject, 'utf-8')

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.login(SENDER_EMAIL, AUTH_CODE)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], message.as_string())
        server.quit()
        print(f"[{datetime.datetime.now()}] 异常发生，告警邮件已送达。")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] 严重错误：告警邮件发送失败 - {e}")

def do_checkin():
    print(f"[{datetime.datetime.now()}] 开始执行 Duckcoding 签到任务...")
    try:
        response = requests.post(CHECKIN_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()

        try:
            result = response.json()
        except ValueError:
            error_msg = f"服务器返回了非预期的格式 (非JSON)。\n状态码: {response.status_code}\n返回内容: {response.text[:200]}"
            print(f"[{datetime.datetime.now()}] 解析异常: {error_msg}")
            send_alert_email("🚨 签到异常：服务器返回格式错误", error_msg)
            return

        print(f"[{datetime.datetime.now()}] 响应内容: {result}")
        print(f"[{datetime.datetime.now()}] 签到成功，不触发邮件。")
        sys.exit(0)

    except requests.exceptions.RequestException as e:
        response_body = e.response.text if hasattr(e, 'response') and e.response is not None else "无响应体"
        error_msg = f"网络协议崩溃或凭证失效。\n错误详情：{e}\n服务器真实报文：{response_body}"
        print(f"[{datetime.datetime.now()}] 网络崩溃: {error_msg}")
        send_alert_email("🚨 签到异常：网络或权限被拒绝", error_msg)

    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"[{datetime.datetime.now()}] 未知崩溃:\n{error_trace}")
        send_alert_email("🚨 签到异常：脚本发生未知崩溃", error_trace)

if __name__ == "__main__":
    do_checkin()
