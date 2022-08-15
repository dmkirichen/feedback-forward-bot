import urllib
from utils import get_url, get_json_from_url


class MessageSender:
    def __init__(self, bot_url, admin_chat_id):
        self.bot_url = bot_url
        self.admin_chat_id = admin_chat_id

    def send_message_to_admins(self, text):
        self.send_text_message(text, self.admin_chat_id)

    def forward_message_to_admins(self, message_id, chat_id):
        url = self.bot_url + "forwardMessage?chat_id={}&from_chat_id={}&message_id={}".format(
            self.admin_chat_id, chat_id, message_id)
        result = get_json_from_url(url)
        return result["result"]["message_id"]

    def send_message(self, content, chat_id):
        if "text" in content:
            text = content["text"]
            self.send_text_message(text, chat_id)
        elif "sticker" in content:
            sticker = content["sticker"]["file_id"]
            self.send_sticker(sticker, chat_id)
        elif "animation" in content:
            animation = content["animation"]["file_id"]
            self.send_animation(animation, chat_id)
        elif "document" in content:
            document = content["document"]["file_id"]
            self.send_document(document, chat_id)
        elif "voice" in content:
            voice = content["voice"]["file_id"]
            self.send_voice(voice, chat_id)
        elif "video" in content:
            video = content["video"]["file_id"]
            self.send_video(video, chat_id)
        elif "photo" in content:
            if isinstance(content["photo"], list):
                photo = content["photo"][0]["file_id"]
                self.send_photo(photo, chat_id)
            else:
                photo = content["photo"]["file_id"]
                self.send_photo(photo, chat_id)
        elif "video_note" in content:
            video_note = content["video_note"]["file_id"]
            self.send_video_note(video_note, chat_id)
        elif "contact" in content:
            first_name = content["contact"]["first_name"]
            phone_number = content["contact"]["phone_number"]
            self.send_contact(first_name, phone_number, chat_id)
        elif "location" in content:
            latitude = content["location"]["latitude"]
            longitude = content["location"]["longitude"]
            self.send_location(latitude, longitude, chat_id)

    def send_text_message(self, text, chat_id):
        text = urllib.parse.quote_plus(text)
        url = self.bot_url + "sendMessage?chat_id={}&text={}".format(chat_id, text)
        get_url(url)

    def send_sticker(self, sticker_id, chat_id):
        url = self.bot_url + "sendSticker?chat_id={}&sticker={}".format(chat_id, sticker_id)
        get_url(url)

    def send_animation(self, animation_id, chat_id):
        url = self.bot_url + "sendAnimation?chat_id={}&animation={}".format(chat_id, animation_id)
        get_url(url)

    def send_document(self, document_id, chat_id):
        url = self.bot_url + "sendDocument?chat_id={}&document={}".format(chat_id, document_id)
        get_url(url)

    def send_voice(self, voice_id, chat_id):
        url = self.bot_url + "sendVoice?chat_id={}&voice={}".format(chat_id, voice_id)
        get_url(url)

    def send_video(self, video_id, chat_id):
        url = self.bot_url + "sendVideo?chat_id={}&video={}".format(chat_id, video_id)
        get_url(url)

    def send_photo(self, photo_id, chat_id):
        url = self.bot_url + "sendPhoto?chat_id={}&photo={}".format(chat_id, photo_id)
        get_url(url)

    def send_video_note(self, video_note_id, chat_id):
        url = self.bot_url + "sendVideoNote?chat_id={}&video_note={}".format(chat_id, video_note_id)
        get_url(url)

    def send_contact(self, first_name, phone_number, chat_id):
        url = self.bot_url + "sendContact?chat_id={}&phone_number={}&first_name={}".format(
            chat_id, phone_number, first_name)
        get_url(url)

    def send_location(self, latitude, longitude, chat_id):
        url = self.bot_url + "sendLocation?chat_id={}&latitude={}&longitude={}".format(chat_id, latitude, longitude)
        get_url(url)
