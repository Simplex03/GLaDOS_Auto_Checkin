from .checkin import CheckinManager
from .notification import TelegramNotifier
import os

def main():
    # 初始化组件
    manager = CheckinManager()
    notifier = TelegramNotifier(
        bot_token=os.getenv("TG_BOT_TOKEN"),
        chat_id=os.getenv("TG_CHAT_ID")
    )

    # 执行签到流程
    try:
        results = manager.run()
        notifier.send_report(results["checkin"], results["status"])
    except Exception as e:
        error_msg = f"❌ 程序执行失败: {str(e)}"
        notifier.send_report([error_msg], [])
