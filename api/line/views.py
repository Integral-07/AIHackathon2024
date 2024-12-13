from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import json

import os
from .utils import message_creater

REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/reply"
HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + str(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
}

class LineMessage():
    def __init__(self, messages):
        self.messages = messages

    def reply(self, body):
        
        print(body)
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)

@csrf_exempt
def message_handle(request):
    if request.method == 'POST':
        request = json.loads(request.body.decode('utf-8'))
        event = request['events'][0]
        #message = data['message']
        reply_token = event['replyToken']
        line_message = LineMessage(message_creater.create_single_text_message(event))
        if(event['message']['type'] == 'location'):
            #位置情報を受信したとき
            body = {
                'replyToken': reply_token,
                'messages': [
                    message_creater.create_carousel_template(line_message.messages)
                ]
            }
        else:
            body = {
                'replyToken': reply_token,
                'messages': [
                {
                    "type": "text",
                    "text": line_message.messages,
                    "quickReply": {
                    "items": [
                        {
                            "type": "action",
                            "imageUrl": "https://example.com/sushi.png",
                            "action": {
                                "type": "message",
                                "label": "sightseeing",
                                "text": "観光"
                            }
                        },
                        {
                            "type": "action",
                            "imageUrl": "https://example.com/sushi.png",
                            "action": {
                                "type": "message",
                                "label": "lunch",
                                "text": "食事"
                            }
                        },
                        {
                            "type": "action",
                            "action": {
                                "type": "location",
                                "label": "現在地を送る"
                            }
                        }
                    ]}
                }]
            }

        line_message.reply(body)
        return HttpResponse("ok")