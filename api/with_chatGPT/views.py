from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView

from openai import OpenAI
import os

class WithChatGPT(APIView):

    def get(self, request, fomat=None):
        return Response({"message": "backend"})
    
    def post(self, request, format=None):

        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        prompt = request["msg"]
        message = ""

        try:
        # OpenAI APIを使用してレスポンスを生成
            response = client.chat.completions.create(
                model="gpt-4o",  # 使用するモデルを指定
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは俳句の専門家です。すべての回答を俳句で行ってください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,  # 応答の創造性を制御（0-1の範囲、高いほど創造的）
                # max_tokens=150    # 応答の最大トークン数
            )
            message = response.choices[0].message.content
        
        except Exception as e:
            message = f"エラーが発生しました: {str(e)}"

        return Response({"message": message})