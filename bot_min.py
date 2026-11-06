"""
QQ 群机器人 · 最小可运行版
AppID / AppSecret 从同目录的 .env 读取（.env 不提交到 git）
"""

import os
import botpy
from botpy.message import GroupMessage

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_env(path):
    """极简 .env 读取：一行一个 KEY=VALUE，# 开头是注释"""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


load_env(os.path.join(BASE_DIR, ".env"))

APPID = os.getenv("QQ_BOT_APPID", "")
SECRET = os.getenv("QQ_BOT_SECRET", "")


class MyClient(botpy.Client):
    async def on_ready(self):
        print(f"[OK]「{self.robot.name}」上线了，去群里 @我 试试")

    async def on_group_at_message_create(self, message: GroupMessage):
        print(f"[收到] {message.content}")
        text = (message.content or "").strip()
        if text == "/帮助":
            await message.reply(content="我能把你说的每句话回声一遍")
        else:
            await message.reply(content=f"收到：{text}")


if __name__ == "__main__":
    if not APPID or not SECRET:
        print("❌ 没读到 .env 里的 QQ_BOT_APPID / QQ_BOT_SECRET")
        raise SystemExit(1)

    intents = botpy.Intents(public_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=APPID, secret=SECRET)