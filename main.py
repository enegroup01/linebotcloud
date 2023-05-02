from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, StickerSendMessage, ImageSendMessage, LocationSendMessage
import requests
import statistics
import json
import time
import os
from gpt_index import GPTSimpleVectorIndex

access_token = '9XCr8nEAGoNl5r+xUC3E4LupOQDi2g0WnMer8dMtrwIi+TGZmdBAjl2wZutBpEcLSrJfuD4+xlUfNywn/21GH+2XGVj+ra2DVCm1a0wNP/Yj1PVKf2cxsceZBbMUPi8qpVzKN8BZGhQgVbkpdnqEWAdB04t89/1O/w1cDnyilFU='
channel_secret = '2c62bd9d16a62c50f6b05c774557ba7b'
os.environ['OPENAI_API_KEY'] = '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'


def linebot(request):
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    try:
        line_bot_api = LineBotApi(access_token)
        handler = WebhookHandler(channel_secret)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']
        msg = json_data['events'][0]['message']['text']
        reply_msg = ''
        with open('vectorIndex.json', 'r') as vectorIndex:
            vIndexData = json.loads(vectorIndex.read())
            vIndex = GPTSimpleVectorIndex.load(vIndexData)
            response = vIndex.query(msg, response_mode='compact')
            reply_msg = response
        text_message = TextSendMessage(text=reply_msg)    # 設定回傳同樣的訊息
        line_bot_api.reply_message(tk, text_message)       # 回傳訊息
    except:
        print('error')
    return 'OK'
