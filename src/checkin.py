import os
import random
import time
import datetime
import requests
from typing import List, Tuple, Dict

class GLaDOSChecker:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; SM-G9750) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15",
        ]

    def _generate_headers(self, cookie: str) -> Dict:
        return {
            "Accept": "application/json, text/plain, */*",
            "Cookie": cookie,
            "User-Agent": random.choice(self.user_agents),
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://glados.rocks"
        }

    def _translate_message(self, raw_message: str) -> str:
        translations = {
            "Please Try Tomorrow": "签到失败，请明天再试 🤖",
            "Checkin Repeats! Please Try Tomorrow": "重复签到，请明天再试 🔁",
        }
        if "Got" in raw_message:
            points = raw_message.split("Got ")[1].split(" Points")[0]
            return f"签到成功，获得 {points} 积分 🎉"
        return translations.get(raw_message, f"未知结果: {raw_message} ❓")

    def check_status(self, cookie: str) -> str:
        url = "https://glados.rocks/api/user/status"
        try:
            response = requests.get(
                url,
                headers=self._generate_headers(cookie),
                timeout=10
            )
            data = response.json()
            days = float(data['data']['leftDays'])
            return f"{days:.1f} 天" if days % 1 else f"{int(days)} 天"
        except Exception as e:
            return f"状态查询失败 ❌ ({str(e)})"

    def checkin(self, cookie: str) -> str:
        url = "https://glados.rocks/api/user/checkin"
        payload = {"token": "glados.one"}
        try:
            response = requests.post(
                url,
                headers=self._generate_headers(cookie),
                json=payload,
                timeout=10
            )
            return self._translate_message(response.json().get("message", ""))
        except Exception as e:
            return f"签到失败 ❌ ({str(e)})"


class CheckinManager:
    def __init__(self):
        self.checker = GLaDOSChecker()
        self.accounts = self._load_accounts()

    def _load_accounts(self) -> List[Tuple[str, str]]:
        accounts = []
        index = 1
        while True:
            email = os.getenv(f"GLADOS_EMAIL_{index}")
            cookie = os.getenv(f"GLADOS_COOKIE_{index}")
            if not (email and cookie):
                break
            accounts.append((email, cookie))
            index += 1
        return accounts

    def run(self) -> Dict[str, List[str]]:
        if not self.accounts:
            raise ValueError("未找到任何账户配置")

        results = {"checkin": [], "status": []}
        for email, cookie in self.accounts:
            time.sleep(random.randint(5, 15))  # 随机延迟
            
            checkin_result = self.checker.checkin(cookie)
            status = self.checker.check_status(cookie)
            
            results["checkin"].append(f"{email}: {checkin_result}")
            results["status"].append(f"{email}: 剩余 {status} 🗓️")
        
        return results
