import os
import time
import asyncio
from aiohttp import web
from utils import get_json_from_url
from database.reply_database import ReplyDatabase
from database.reply_file_database import ReplyFileDatabase
from message_sender import MessageSender


TOKEN = os.environ.get("TOKEN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

auto_messages = {"start": """Доброго дня✨🍃
Ви написали у наш бот: де можете залишити свій відгук, задати питання чи обговорити співпрацю/рекламу🌿
Чим я можу вам допомогти?🌱""",
                 "got_message": "Ми отримали ваше повідомлення, очікуйте на відповідь"}


class FeedbackForwardBot:
    def __init__(self, token: str, admin_chat_id: int):
        self._app = web.Application()
        self._app.add_routes([web.post('/', self._handle_update)])

        self._url = "https://api.telegram.org/bot{}/".format(token)
        self._admin_chat_id = admin_chat_id
        self._db: ReplyDatabase = ReplyFileDatabase("database/replies.csv", max_entries=1000000)
        self._ms: MessageSender = MessageSender(self._url, self._admin_chat_id)
        self._cont_types = ["text", "sticker", "animation", "document", "voice",
                            "video", "photo", "video_note", "contact", "location"]

    def set_webhook(self, webhook_url: str):
        """Set webhook from bot API telegram to 'webhook_url'."""
        url = self._url + f"setWebHook?url={webhook_url}"
        js = get_json_from_url(url)
        return js

    def get_updates(self, offset=None):
        """Used for polling, deprecated for our webhook usage."""
        url = self._url + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        js = get_json_from_url(url)
        return js

    @staticmethod
    def _get_last_update_id(updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def _check_if_dict_has_cont_type(self, d: dict):
        return any([content_type in d for content_type in self._cont_types])

    def _handle_user_update(self, update):
        print("got a message from user chat")
        if "message" in update:
            message = update["message"]
            if self._check_if_dict_has_cont_type(message):
                chat_id = message["chat"]["id"]
                user_message_id = message["message_id"]
                if "text" in message:
                    if message["text"] == "/start":
                        # Automatic message at the start of interaction with a bot
                        self._ms.send_text_message(auto_messages["start"], chat_id)
                        return
                # Forwarding message to admin chat and printing to user that we got his message
                chat_message_id = self._ms.forward_message_to_admins(user_message_id, chat_id)
                self._db.add_entry(str(chat_message_id), str(chat_id))
                self._ms.send_text_message(auto_messages["got_message"], chat_id)

    def _handle_admin_update(self, update):
        print("got a message from admin chat")
        if "message" in update:
            if "reply_to_message" in update["message"]:
                reply_message_id = update["message"]["reply_to_message"]["message_id"]
                chat_id = self._db.get_entry(str(reply_message_id))
                if not chat_id:
                    print(f"error: couldn't send message from admins to chat_id={chat_id}")
                else:
                    print(f"sending message from admins to chat_id={chat_id}")
                self._ms.send_message(update["message"], chat_id)

    async def _handle_update(self, request):
        update = await request.json()
        print(update)
        if "message" in update:
            if str(update["message"]["chat"]["id"]) == str(self._admin_chat_id):
                self._handle_admin_update(update)
            else:
                self._handle_user_update(update)
        return web.Response(text="got your request to '/'")

    def mainloop(self):
        web.run_app(self._app)


if __name__ == '__main__':
    if TOKEN is None or ADMIN_CHAT_ID is None or WEBHOOK_URL is None:
        print("you need to set TOKEN, ADMIN_CHAT_ID and WEBHOOK_URL environment variables")
        exit(1)

    print("Starting the bot...")
    bot = FeedbackForwardBot(TOKEN, ADMIN_CHAT_ID)
    bot.set_webhook(WEBHOOK_URL)
    bot.mainloop()
