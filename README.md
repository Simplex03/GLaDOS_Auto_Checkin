# GLaDOS Auto Checkin

自动签到GLaDOS账户并通过Telegram通知

## 功能特性

- 每日自动签到（北京时间16:00）
- 账户状态查询
- Telegram通知结果
- 代理支持
- 完善的错误处理

## 配置指南

1. Fork本仓库
2. 添加GitHub Secrets：
   - `GLADOS_EMAIL`: 你的GLaDOS注册邮箱
   - `GLADOS_COOKIE`: 从浏览器获取的Cookie
   - `TG_BOT_TOKEN`: Telegram Bot Token
   - `TG_CHAT_ID`: 接收通知的Chat ID
3. 手动触发工作流测试：
   - 在Actions标签页手动运行工作流
