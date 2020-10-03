# messageconnector.py
An SMS and Messages Connector app that integrates TelegramBotPy with Vonage and Twilio

This will be a running document - but here's some basic instructions to get started

Python 3 is required
The following basic python packages are required to install (preferably using pip3 - example: `pip3 install telgram`):

1. telebot
2. telegram
3. requests
4. flask
5. twilio
6. nexmo(optional)
7. sqllite3
8. pathlib

Directions:
1. Pull down the repo
2. install packages noted above
3. setup a telegram telebot
4. setup a twilio account - you will need to setup a phone number in twilio as well
5. optional: setup a vonage account - note: for credentials file, these will still need placeholders for now
6. setup some kind of DNS forwarder for webhooks to manage your localhost instance of flask(I used NGROK)
7. setup credentials.py file
  here's an example using all required properties
  **a helpful note:** *you will need to go through the required steps in twilio, vonage, and telegram to setup required token and secrets for each(I have not given proper examples of these **but I plan to in the future**)*
  ```
  bot_token = "23423:asdfas"
  URL = "https://examplednsurl.ngrok.co"
  api_id = "231412"
  api_hash = "asdfasdfasdfas"
  vonage_secret = "asdfasdfasd"
  vonage_token = "dafasd"
  twilio_token = "asdfasdf"
  twilio_sid = "adsfasdfas"
  outbound_number = "15555555555{note:this should be your twilio phone number"
  principal_number = "15555555555(note:this can be the same number as your twilio - but it can also be another number used to forward texts - e.g. google voice)"
  telegram_api_id = "23423423"
  telegram_api_hash= "adsfasdf3242342"
  ```
8. execute the application by running main.py(e.g. `python3 main.py`)
