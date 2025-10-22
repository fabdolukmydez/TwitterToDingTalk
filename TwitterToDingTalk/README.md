# TwitterToDingTalk

轮询监听指定 Twitter 用户的新推文与转推，并自动转发到钉钉机器人。

## 使用方式

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 设置环境变量：
   ```bash
   export TWITTER_BEARER_TOKEN="你的Twitter Bearer Token"
   export TWITTER_USER_ID="目标用户的数值型ID"
   export DINGTALK_WEBHOOK="钉钉群机器人Webhook"
   export POLL_INTERVAL=60  # 可选，默认60秒
   ```

3. 运行脚本：
   ```bash
   python main.py
   ```

4. GitHub 将识别此项目为 Python 项目。
