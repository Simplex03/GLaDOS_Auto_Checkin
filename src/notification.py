import datetime
import requests

class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str):
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.chat_id = chat_id

    def _current_time(self) -> str:
        beijing_time = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        return beijing_time.strftime("%Y-%m-%d %H:%M")

    def send_report(self, checkin_results: List[str], status_results: List[str]):
        time_str = self._current_time()
        
        message = [
            f"🕒 执行时间: {time_str}",
            "🔔 签到结果:",
            *checkin_results,
            "\n⏳ 账户状态:",
            *status_results,
            "\n✅ 任务完成"
        ]

        payload = {
            "chat_id": self.chat_id,
            "text": "\n".join(message),
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(
                f"{self.base_url}/sendMessage",
                json=payload,
                timeout=10
            )
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Telegram 通知发送失败: {str(e)}")
