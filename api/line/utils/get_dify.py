import requests
import os, json

# Dify APIのベースURL
BASE_URL = "https://api.dify.ai/v1/chat-messages"
API_KEY = os.getenv("DIFY_API")
if not API_KEY:
    raise ValueError("DIFY_API environment variable is not set.")

def get_dify_response(query: str, user: str, conversation_id="") -> str:
    """
    Dify APIにリクエストを送信し、応答を取得する関数

    :param query: ユーザーの質問
    :param user: ユーザー識別子
    :return: APIからの応答テキスト
    """
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "conversation_id": conversation_id,
        "user": user
    }
    
    response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    
    return response.json()['answer']