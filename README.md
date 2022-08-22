# Feedback Forward Telegram Bot

Asynchronous telegram bot that forwards messages from the chat with a user to admin chat, where admins can reply to all messages.

### Requirements
Python 3.8+
- requests==2.26.0
- urllib3==1.26.7
- filelock==3.7.1
- asyncio~=3.4.3
- aiohttp~=3.8.1
- pytest~=7.1.2

### Usage
Webhooks require the server to be publicly available and have domain name.

You need to set TOKEN, ADMIN_CHAT_ID and WEBHOOK_URL environment variables on the server, which will run the bot.

To run the script, use: 
```bash
TOKEN="token" ADMIN_CHAT_ID="admin-chat-id" WEBHOOK_URL="webhook-url" python3.8 bot.py
```

