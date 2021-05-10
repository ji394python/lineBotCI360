import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent,MessageEvent, TextMessage, TextSendMessage
from random import randint
import requests 
from bs4 import BeautifulSoup


app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))
textRandom = ['[胺基酸多巴胺葡萄糖碇]','[來人!餵公子吃餅]','[這個我們下次再開一集視頻來解釋！]']


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)  #官方拿來驗證linePlatform的訊息是否真的為linePlatform發來
        except InvalidSignatureError:
            abort(400)

        return "OK"

##監聽程序，前面要處理的事件類別，後面放要用甚麼格式來回復訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    get_userId = event.source
    r = requests.get('https://www.ptt.cc/bbs/Stock/index.html')
    r = BeautifulSoup(r.text)
    script = r.select('.title')[0].text.strip()
    # Send To Line
    reply = TextSendMessage(text=f" {textRandom[randint(0,2)]} \n {script} {get_message} \n {get_userId}")
    line_bot_api.reply_message(event.reply_token, reply)
    line_bot_api.push_message('U59c9b989be10bed54b972766530b9fb9', TextSendMessage(text='Hello World!'))

@handler.add(FollowEvent)
def handle_message(event):
    # Send To Line
    reply = TextSendMessage(text=f"[感謝您加我為好友QQ]")
    line_bot_api.reply_message(event.reply_token, reply)

