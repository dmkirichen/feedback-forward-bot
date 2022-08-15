import json
import time
from utils import get_json_from_url
from database.reply_database import ReplyDatabase
from database.reply_file_database import ReplyFileDatabase
from message_sender import MessageSender


with open("./credentials.json", "r") as f:
    credentials_data = json.load(f)

TOKEN = credentials_data["TOKEN"]
ADMIN_CHAT_ID = credentials_data["ADMIN_CHAT_ID"]

# PORT = os.getenv("PORT", default="5000")

auto_messages = {"start": """Доброго дня✨🍃
Ви написали у наш бот: де можете залишити свій відгук, задати питання чи обговорити співпрацю/рекламу🌿
Чим я можу вам допомогти?🌱""",
                 "got_message": "Ми отримали ваше повідомлення, очікуйте на відповідь"}


class FeedbackForwardBot:
    def __init__(self, token: str, admin_chat_id: int):
        self._url = "https://api.telegram.org/bot{}/".format(token)
        self._admin_chat_id = admin_chat_id
        self._db: ReplyDatabase = ReplyFileDatabase("database/replies.csv", max_entries=1000000)
        self._ms: MessageSender = MessageSender(self._url, self._admin_chat_id)
        self._cont_types = ["text", "sticker", "animation", "document", "voice",
                            "video", "photo", "video_note", "contact", "location"]

    def get_updates(self, offset=None):
        url = self._url + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        js = get_json_from_url(url)
        return js

    @staticmethod
    def get_last_update_id(updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def check_if_dict_has_cont_type(self, d: dict):
        return any([content_type in d for content_type in self._cont_types])

    def handle_user_update(self, update):
        print("got a message from user chat")
        if "message" in update:
            message = update["message"]
            if self.check_if_dict_has_cont_type(message):
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

    def handle_admin_update(self, update):
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

    def handle_updates(self, updates):
        for update in updates["result"]:
            if "message" in update:
                if update["message"]["chat"]["id"] == self._admin_chat_id:
                    self.handle_admin_update(update)
                else:
                    self.handle_user_update(update)

    def mainloop(self):
        last_update_id = None
        while True:
            updates = self.get_updates(last_update_id)
            print(updates)
            if len(updates["result"]) > 0:
                print(f"\n{updates}")
                last_update_id = self.get_last_update_id(updates) + 1
                self.handle_updates(updates)
            time.sleep(0.5)


if __name__ == '__main__':
    print("Starting the bot...")
    bot = FeedbackForwardBot(TOKEN, ADMIN_CHAT_ID)
    bot.mainloop()
