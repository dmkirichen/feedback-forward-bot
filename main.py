"""
Розроблено Дімасіком для "У Куточку в Таверні".
Тестувальники без яких робота була б неможлива
- Поет нової України і романтик в душі, Женя
- Дивовижна і чудова, Поляна
- Scarlet, яка попросила залишитись анонімною
Дякуємо Сергію Дамбесту за допомогу.
"""
import os
import json
import requests
import time
import urllib
from database import ReplyDatabase

with open("./credentials.json", "r") as f:
    credentials_data = json.load(f)

TOKEN = credentials_data["TOKEN"]
ADMIN_CHAT_ID = credentials_data["ADMIN_CHAT_ID"]
WEBHOOK_URL = credentials_data["WEBHOOK_URL"]
PORT = os.getenv("PORT", default="5000")
# URL = "https://api.telegram.org:{}/bot{}/".format(PORT, TOKEN)
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
db = ReplyDatabase("replies.csv", max_entries=10)


def get_url(url):
    url_str = f"{url}"
    print(url_str)
    response = requests.get(url_str)

    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(f"{url}")
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def handle_user_update(update):
    print("got a message from user chat")
    if "message" in update:
        if "text" in update["message"] or \
           "sticker" in update["message"] or \
           "animation" in update["message"] or \
           "document" in update["message"] or \
           "voice" in update["message"] or \
           "video" in update["message"] or \
           "photo" in update["message"] or \
           "video_note" in update["message"] or \
           "contact" in update["message"] or \
           "location" in update["message"]:
            chat_id = update["message"]["chat"]["id"]
            user_message_id = update["message"]["message_id"]
            chat_message_id = forward_message_to_admins(user_message_id, chat_id)
            db.add_entry(str(chat_message_id), str(chat_id))
            send_message("Ми отримали ваше повідомлення, очікуйте на відповідь", chat_id)


def handle_admin_update(update):
    print("got a message from admin chat")
    if "message" in update:
        if "reply_to_message" in update["message"]:
            reply_message_id = update["message"]["reply_to_message"]["message_id"]
            chat_id = db.get_entry(str(reply_message_id))
            if not chat_id:
                print(f"error: chat_id={chat_id}")
            print(f"chat_id={chat_id}")
            
            if "text" in update["message"]:
                text = update["message"]["text"]
                send_message(text, chat_id)
            elif "sticker" in update["message"]:
                sticker = update["message"]["sticker"]["file_id"]
                send_sticker(sticker, chat_id)
            elif "animation" in update["message"]:
                animation = update["message"]["animation"]["file_id"]
                send_animation(animation, chat_id)
            elif "document" in update["message"]:
                document = update["message"]["document"]["file_id"]
                send_document(document, chat_id)
            elif "voice" in update["message"]:
                voice = update["message"]["voice"]["file_id"]
                send_voice(voice, chat_id)
            elif "video" in update["message"]:
                video = update["message"]["video"]["file_id"]
                send_video(video, chat_id)
            elif "photo" in update["message"]:
                if isinstance(update["message"]["photo"], list):
                    photo = update["message"]["photo"][0]["file_id"]
                    send_photo(photo, chat_id)
                else:  
                    photo = update["message"]["photo"]["file_id"]
                    send_photo(photo, chat_id)
            elif "video_note" in update["message"]:
                video_note = update["message"]["video_note"]["file_id"]
                send_video_note(video_note, chat_id)
            elif "contact" in update["message"]:
                first_name = update["message"]["contact"]["first_name"]
                phone_number = update["message"]["contact"]["phone_number"]
                send_contact(first_name, phone_number, chat_id)
            elif "location" in update["message"]:
                latitude = update["message"]["location"]["latitude"]
                longitude = update["message"]["location"]["longitude"]
                send_location(latitude, longitude, chat_id)


def handle_updates(updates):
    for update in updates["result"]:
        if "message" in update:
            if update["message"]["chat"]["id"] == ADMIN_CHAT_ID:
                handle_admin_update(update)
            else:
                handle_user_update(update)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?chat_id={}&text={}".format(chat_id, text)
    get_url(url)


def send_sticker(sticker_id, chat_id):
    url = URL + "sendSticker?chat_id={}&sticker={}".format(chat_id, sticker_id)
    get_url(url)


def send_animation(animation_id, chat_id):
    url = URL + "sendAnimation?chat_id={}&animation={}".format(chat_id, animation_id)
    get_url(url)


def send_document(document_id, chat_id):
    url = URL + "sendDocument?chat_id={}&document={}".format(chat_id, document_id)
    get_url(url)


def send_voice(voice_id, chat_id):
    url = URL + "sendVoice?chat_id={}&voice={}".format(chat_id, voice_id)
    get_url(url)


def send_video(video_id, chat_id):
    url = URL + "sendVideo?chat_id={}&video={}".format(chat_id, video_id)
    get_url(url)


def send_photo(photo_id, chat_id):
    url = URL + "sendPhoto?chat_id={}&photo={}".format(chat_id, photo_id)
    get_url(url)


def send_video_note(video_note_id, chat_id):
    url = URL + "sendVideoNote?chat_id={}&video_note={}".format(chat_id, video_note_id)
    get_url(url)


def send_contact(first_name, phone_number, chat_id):
    url = URL + "sendContact?chat_id={}&phone_number={}&first_name={}".format(chat_id, phone_number, first_name)
    get_url(url)


def send_location(latitude, longitude, chat_id):
    url = URL + "sendLocation?chat_id={}&latitude={}&longitude={}".format(chat_id, latitude, longitude)
    get_url(url)


def forward_message_to_admins(message_id, chat_id):
    url = URL + "forwardMessage?chat_id={}&from_chat_id={}&message_id={}".format(ADMIN_CHAT_ID, chat_id, message_id)
    result = get_json_from_url(url)
    return result["result"]["message_id"]


def send_message_to_admins(text):
    send_message(text, ADMIN_CHAT_ID)
    # text = urllib.parse.quote_plus(text)
    # url = URL + "sendMessage?text={}&chat_id={}".format(text, ADMIN_CHAT_ID)
    # get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        print(updates)
        if len(updates["result"]) > 0:
            print(f"\n{updates}")
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    print("Bot has started.")
    # get_url(URL + f"setWebhook?url={WEBHOOK_URL}{TOKEN}")
    db.show_contents()
    main()
