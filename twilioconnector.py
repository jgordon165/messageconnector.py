import json
import telebot
import telegram
import requests
import telemessageutility
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from types import SimpleNamespace
from credentials import twilio_token, twilio_sid, outbound_number
from twilio.rest import Client

class Connector() :
    global teleUtility
    teleUtility = telemessageutility.MessageUtility()

    global TOKEN
    global NUMBER
    global ACCOUNT

    TOKEN = twilio_token
    NUMBER = outbound_number
    ACCOUNT = twilio_sid

    def initializeInboundSMS(self, app, TOKEN) :
        global bot
        bot = telegram.Bot(token=TOKEN)
        @app.route("/webhooks/inbound-mms", methods=['GET', 'POST'])
        def sms_reply():
            """Respond to incoming calls with a MMS message."""
            # Start our TwiML response
            resp = MessagingResponse()

            if request.is_json:
                self.recievesms(request.get_json(), TOKEN)
            else:
                data = dict(request.form) or dict(request.args)
                self.recievesms(data, TOKEN)

            return str(resp)

    def sendsms(self, number, msg) :
        client = Client(ACCOUNT, TOKEN)

        message = client.messages.create(
                                    body=msg,
                                    from_='+{}'.format(NUMBER),
                                    to='+{}'.format(number)
                                )

    def sendmms(self, number, msg, url) :
        print(url)
        client = Client(ACCOUNT, TOKEN)

        message = client.messages.create(
                                    body=msg,
                                    from_='+{}'.format(NUMBER),
                                    media_url=[url],
                                    to='+{}'.format(number)
                                )

    def recievesms(self, data, token) :
        print(data)
        chatId = teleUtility.getChatId(data['From'].replace('+',''), token)
        body = data['Body']

        if chatId == teleUtility.getJunkId(token) :
            if "NumMedia" in data and int(data["NumMedia"]) > 0:
                self.sendImages(data, '{number}'.format(number=data['From'].replace('+','')), chatId)
            bot.sendMessage(chat_id=chatId, text='{number}:{text}'.format(number=data['From'].replace('+',''), text=data['Body']))
        elif chatId == teleUtility.getGroupId(token) :
            if "NumMedia" in data and int(data["NumMedia"]) > 0:
                self.sendImages(data, '', chatId)
            bot.sendMessage(chat_id=chatId, text=''.format(data['Body']))
        elif chatId != None:
            if "NumMedia" in data and int(data["NumMedia"]) > 0:
                self.sendImages(data, 'Recieved', chatId)
            bot.sendMessage(chat_id=chatId, text='Recieved:{}'.format(data['Body']))
        else:
            bot.sendMessage(chad_id='channel_junk', text='Channel or group not found for number:{}'.format(data['From'].replace('+','')))

    def sendImages(self, data, text, chatId) :
        text += ':{text}'
        if "NumMedia" in data:
            for x in range(int(data['NumMedia'])):
                bot.sendMessage(chat_id=chatId, text=text.format(text=data['MediaUrl{}'.format(x)]))