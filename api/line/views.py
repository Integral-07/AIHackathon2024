#from . import line_config

from rest_framework.response import Response
from rest_framework.views import APIView

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

class Line(APIView):
    
    def __init__(self):

        self.line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))#line_config.LINE_CHANNEL_ACCESS_TOKEN)    
        self.handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))#line_config.LINE_CHANNEL_SECRET)    

    def handle_message(self, event):
        """
        メッセージイベントを処理し、オウム返しを返信する
        """
        if event.reply_token == "00000000000000000000000000000000":
            return

        self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

    def post(self, request, *args, **kwargs):
        """
        LINEからのWebhookリクエストを処理する
        """
        signature = request.META.get("HTTP_X_LINE_SIGNATURE")
        if not signature:
            return Response({"error": "Signature not found"}, status=400)

        body = request.body.decode("utf-8")

        try:
            self.handler.handle(body, signature)
        except InvalidSignatureError:
            return Response({"error": "Invalid signature"}, status=400)

        return Response({"message": "OK"})

    def get(self, request, format=None):
        return Response({"message": "backend"})