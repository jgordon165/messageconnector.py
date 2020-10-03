import json
import telebot
import telegram
import vonageconnector
import twilioconnector
import telemessageutility
import re
import time
import emoji
import requests

from types import SimpleNamespace
from flask import Flask, request, jsonify
from pprint import pprint
from credentials import bot_token, URL, api_id, api_hash, principal_number

global bot
global TOKEN
global teleUtility
global NUMBER
TOKEN = bot_token
teleUtility = telemessageutility.MessageUtility()
NUMBER = principal_number

app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)

vonageconnector = vonageconnector.Connector()
#with Twilio now setup no longer need to use vonage connector for inbounds
vonageconnector.initializeInboundSMS(app, TOKEN)

twilioconnector = twilioconnector.Connector()
twilioconnector.initializeInboundSMS(app, TOKEN)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   print(request.data)
   update = telegram.Update.de_json(request.get_json(force=True), bot)
   
   print(update)

   # Telegram understands UTF-8, so encode text for unicode compatibility
   global text
   global fileid
   text = None
   fileid = None
   if update.channel_post!=None:
       text = update.channel_post.text
       chat_id = update.channel_post.chat.id
       if update.channel_post.chat.username!=None:
        number = str(update.channel_post.chat.username).split('_')[1]
       else:
        number = teleUtility.getChatNumberFromName(chat_id)
       msg_id = update.channel_post.message_id

       if update.channel_post.document!=None:
           fileid = update.channel_post.document.file_id
           text = update.channel_post.caption
       elif update.channel_post.photo!=None and len(update.channel_post.photo) > 0:
           fileid = update.channel_post.photo[0].file_id
           text = update.channel_post.caption
   else:
       if update.message.text!=None:
        text = update.message.text
       chat_id = update.message.chat.id
       msg_id = update.message.message_id
       number = NUMBER

   # the first time you chat with the bot AKA the welcoming message
   if text == "/start":
       # print the welcoming message
       bot_welcome = """
       messages.py initiated
       """
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
   elif text != None and str.__contains__(text, "/persist"):
       print("try to persist number")

       txtIts = text.split(' ')
       number = txtIts[1]
       newChatId = teleUtility.getChatId(number, TOKEN)
       if newChatId != None:
            bot.sendMessage(chat_id=newChatId, text='BOT:ChatId found for number:{number} - chatid:{chatid}'.format(number=number, chatid=newChatId))
       else:
            bot.sendMessage(chad_id='joel_junk', text='Channel or group not found for number:{}'.format(number))
   elif text != None and str.__contains__(text, "/cleanup"):
       print("try to clean up")
       
       txtIts = text.split(':')
       print(txtIts)
       if len(txtIts) == 3:
           number = txtIts[1]
           newChatId = teleUtility.getChatId(number, TOKEN)
           if newChatId != None:
                bot.sendMessage(chat_id=newChatId, text='Recieved:{}'.format(txtIts[2]))
           else:
               bot.sendMessage(chad_id='joel_junk', text='Channel or group not found for number:{}'.format(number))
   else:
       try:
           #include emojis
           if(text != None and str.__contains__(text, ":")):
               textRegex = br'text\":\"(.*)\"'
               textResult = re.search(textRegex, request.data) 

               text = textResult.group(1)

           if fileid != None:
               print("include media")
               print(number)
               filepath = teleUtility.getFilePath('https://api.telegram.org/bot{TOKEN}/getFile?file_id={FILEID}'.format(TOKEN=TOKEN, FILEID=fileid))
               twilioconnector.sendmms(number, text, 'https://api.telegram.org/file/bot{TOKEN}/{FILEPATH}'.format(TOKEN=TOKEN, FILEPATH=filepath))
           elif text != None:
               print("try to send sms")   
               print(number)      
               print(text)
               twilioconnector.sendsms(number, text)
       except Exception as error:
           # if things went wrong
           print(error)
           print("There was a problem in the name you used, please enter different name")

   return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.set_webhook(url='https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}/{TOKEN}'.format(URL=URL, TOKEN=TOKEN))
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"

@app.route('/')
def index():
   return '.'

app.run(port=3000,threaded=True)