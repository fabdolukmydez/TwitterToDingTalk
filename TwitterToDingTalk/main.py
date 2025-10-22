# TwitterToDingTalk/main.py
import os
import time
import requests
import tweepy
from datetime import datetime, timezone

# =============== 配置 ===============
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TARGET_USER_ID = os.getenv("TWITTER_USER_ID")
DINGTALK_WEBHOOK = os.getenv("DINGTALK_WEBHOOK")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 60))  # 轮询间隔秒数

# =============== 初始化 ===============
client = tweepy.Client(bearer_token=BEARER_TOKEN)
last_seen_id = None

def send_to_dingtalk(username, user_id, created_at, text, tweet_url):
    message = {
        "msgtype": "markdown",
        "markdown": {
            "title": "Twitter 推文更新",
            "text": f"**{username} (@{user_id})**\n
🕒 {created_at}\n
📄 {text}\n
🔗 [查看推文]({tweet_url})"
        }
    }
    resp = requests.post(DINGTALK_WEBHOOK, json=message)
    print("钉钉返回：", resp.status_code, resp.text)

def fetch_latest_tweets():
    global last_seen_id
    tweets = client.get_users_tweets(
        id=TARGET_USER_ID,
        tweet_fields=["created_at"],
        max_results=5
    )
    if not tweets.data:
        return

    new_tweets = []
    for tweet in tweets.data:
        if last_seen_id is None or tweet.id > last_seen_id:
            new_tweets.append(tweet)

    if not new_tweets:
        return

    new_tweets.sort(key=lambda t: t.id)

    user = client.get_user(id=TARGET_USER_ID).data
    for tweet in new_tweets:
        tweet_url = f"https://twitter.com/{user.username}/status/{tweet.id}"
        send_to_dingtalk(user.username, user.id, tweet.created_at, tweet.text, tweet_url)

    last_seen_id = new_tweets[-1].id

if __name__ == "__main__":
    print("🚀 启动 Twitter → 钉钉 转发服务（轮询模式）")
    while True:
        try:
            fetch_latest_tweets()
        except Exception as e:
            print("❌ 错误：", e)
        time.sleep(POLL_INTERVAL)
