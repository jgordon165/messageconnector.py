import json
import telebot
import telegram
import nexmo
import requests
import databaseutility
from types import SimpleNamespace
from credentials import telegram_api_id, telegram_api_hash

from telethon import TelegramClient

class MessageUtility() : 
    global db
    db = databaseutility.DatabaseUtility()
    def getChatNumberFromName(self, id) :
        return db.get_conversation_name(id)

    def getChatId(self,key,token) :
        conv = db.get_conversation(key, 'channel')
        chat_id = None
        if conv == {}:
            r = requests.post('https://api.telegram.org/bot{token}/sendMessage?chat_id=@channel_{channelName}&text=BOT:acquiringId'.format(channelName=key, token=token))
            print(r.content)
            data = json.loads(r.content, object_hook=lambda d: SimpleNamespace(**d))

            if hasattr(data, 'result'):
                chat_id = data.result.chat.id
            #dump into junk channel
            else:
                chat_id = self.getJunkId(token)
        else:
            chat_id = conv['chat_id']

        if chat_id != None:
            db.create_conversation(chat_id, key, 'channel')

        return chat_id

    def getJunkId(self, token) :
        conv = db.get_conversation('junk', 'channel')
        print('dict')
        print(conv)
        junk_id = None
        if conv == {}:
            #will need to create this channel using your bot token
            r = requests.post('https://api.telegram.org/bot{token}/sendMessage?chat_id=@channel_junk&text=BOT:acquiringId'.format(token=token))
            print(r.content)
            data = json.loads(r.content, object_hook=lambda d: SimpleNamespace(**d))
            junk_id = data.result.chat.id
        else:
            junk_id = conv['chat_id']

        if junk_id != None:
            db.create_conversation(junk_id, 'junk', 'channel')
        return junk_id

    def getFilePath(self, url) : 
        r = requests.post(url)
        print(r.content)
        data = json.loads(r.content, object_hook=lambda d: SimpleNamespace(**d))
        return data.result.file_path
