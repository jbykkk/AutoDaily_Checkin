# DuckCoding Auto Check-in

这是一个用于 DuckCoding 中转站的 Python 自动签到脚本。部署在 Linux 服务器上后，可以通过 Crontab 实现每日定时签到，防止因遗忘而断签。

## 📋 功能特点

* **API 模拟**：直接调用后端 API 接口，无需运行浏览器（Headless），资源占用极低。
* **状态检测**：自动识别“签到成功”、“今日已签到”或“Cookie 失效”等状态。
* **日志记录**：支持将运行结果输出到日志文件，便于后期排查。

## 🛠️ 环境依赖

* **Python 3.x**
* **Python 库**：`requests`

### 安装依赖
如果你没有安装 `requests` 库，请运行以下命令：
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
30 07 * * * /usr/bin/python3 /home/user/projects/daily_checkin/duck_checkin.py >> /home/user/projects/daily_checkin/checkin.log 2>&1
```

- 30 07 * * *: 每天 07:30 执行。
- .../checkin.log: 将标准输出追加到日志文件。
- 2>&1: 将错误信息（如有报错）也重定向到日志文件中，方便排查。

输入以下命令，确认任务已添加成功：
```bash
crontab -l
```

## ⚠️ 安全提示
- Session Cookie 有效期：如果日志中出现登录失效提示，大概率是 Cookie 过了有效期，请更新 Cookie。
- 不要在任何公共场合暴露你的真实 Session Cookie，有时这比暴露密码还危险！