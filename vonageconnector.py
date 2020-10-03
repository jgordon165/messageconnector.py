import json
import telebot
import telegram
import nexmo
import requests
import telemessageutility
from types import SimpleNamespace
from flask import Flask, request, jsonify
from pprint import pprint
from credentials import vonage_token, vonage_secret, outbound_number

class Connector() :
    global teleUtility
    teleUtility = telemessageutility.MessageUtility()

    global TOKEN
    global NUMBER
    global ACCOUNT

    TOKEN = vonage_token
    NUMBER = outbound_number
    ACCOUNT = vonage_secret

    def initializeInboundSMS(self, app, TOKEN) :
        global bot
        bot = telegram.Bot(token=TOKEN)
        @app.route('/webhooks/inbound-sms', methods=['GET', 'POST'])
        def inbound_sms():
            # if request.is_json:
            #     self.recievesms(request.get_json(), TOKEN)
            # else:
            #     data = dict(request.form) or dict(request.args)
            #     self.recievesms(data, TOKEN)

            return ('', 204)

    def sendsms(self, number, msg) :
        client = nexmo.Client(key=TOKEN, secret=ACCOUNT)
        client.send_message({
        'from': NUMBER,
        'to':number,
        'text': msg
        })

    def recievesms(self, data, token) :
        print(data)
        chatId = teleUtility.getChatId(data['msisdn'], token)
        if chatId == teleUtility.getJunkId(token) :
            bot.sendMessage(chat_id=chatId, text='{number}:{text}'.format(number=data['msisdn'], text=data['text']))
        elif chatId == teleUtility.getGroupId(token) :
            bot.sendMessage(chat_id=chatId, text='{}'.format(data['text']))
        else:
            bot.sendMessage(chat_id=chatId, text='Recieved:{}'.format(data['text']))