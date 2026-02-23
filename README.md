# Auto Check-in

中转站的 Python 自动签到脚本，支持异常邮件告警。部署在服务器后可通过定时任务实现每日签到。

## 📋 功能特点

* **API 模拟**：直接调用后端 API 接口，无需浏览器，资源占用极低。
* **邮件告警**：签到失败时自动发送邮件通知。
* **多层异常检测**：
  * HTTP 层：401/403/500 等状态码
  * 业务层：非 JSON 响应格式
  * 网络层：超时、DNS 失败
  * 未知异常：捕获所有未预期错误
* **日志记录**：带时间戳的运行日志，便于排查问题。

## 🛠️ 环境依赖

* **Python 3.x**
* **Python 库**：`requests`

### 安装依赖
```bash
pip3 install requests
```
## 定时任务设置

1、确认解释器路径：
```bash
which python3
```

2、编辑 Crontab：
```bash
crontab -e
```

3、写入定时规则：
```bash
30 07 * * * /usr/bin/python3 /home/user/projects/daily_checkin/checkin_with_emailsend.py >> /home/user/projects/daily_checkin/checkin.log 2>&1
```

- 30 07 * * *: 每天 07:30 执行。
- .../checkin.log: 将标准输出追加到日志文件。
- 2>&1: 将错误信息（如有报错）也重定向到日志文件中，方便排查。

4、确认任务已添加：
```bash
crontab -l
```

## ⚙️ 配置说明

编辑脚本，替换以下配置项：

| 配置项 | 说明 |
|--------|------|
| `SENDER_EMAIL` | 发件邮箱地址（建议使用 163 邮箱） |
| `AUTH_CODE` | 邮箱 SMTP 授权码（非登录密码） |
| `RECEIVER_EMAIL` | 接收告警的邮箱地址 |
| `cookie` | 中转站的 session cookie |

**获取 163 授权码方法**：登录 163 邮箱 → 设置 → POP3/SMTP/IMAP → 开启 SMTP 服务 → 生成授权码。

## ⚠️ 安全提示
- Session Cookie 有有效期，如出现登录失效需重新获取。
- 不要在公开场合暴露 Cookie 或 SMTP 授权码。