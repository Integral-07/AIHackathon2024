from openai import OpenAI
from .get_dify import get_dify_response
import json

#client = OpenAI(api_key=os.getenv("OPENAI_ASSISTANT_API_KEY"))

def create_carousel_template(data_json):
    columns = []
    data = json.loads(data_json)
    idx = 0
    while True:
        try:
            #image_url = get_dify_response(user="Re", query=f"{data[idx]["place"]}の画像のURLを返して")

            columns.append({
            "thumbnailImageUrl": "https://www.fuji-net.co.jp/wp/wp-content/uploads/2022/08/0.jpg",
            "imageBackgroundColor": "#FFFFFF",
            "title": data[idx]["place"],
            "text": data[idx]["description"],
            "defaultAction":{

                "type": "uri",
                "label": "View on GoogleMap",
                "uri": data[idx]["gmap"]
            },
            "actions": [
                {
                    "type": "uri",
                    "label": "View on GoogleMap",
                    "uri": data[idx]["gmap"]
                }
            ]
            })

            idx += 1;
        except IndexError:
            break

    return {
        "type": "template",
        "altText": "recommendation",
        "template": {
            "type": "carousel",
            "columns": columns,
            "imageAspectRatio": "rectangle",
            "imageSize": "cover"
        }
    }

def create_single_text_message(event):
    
    response = ""
    #thread = client.beta.threads.create()

    try:
        if(event['type'] == "message"):
            if(event['message']['type'] == "text"):

                query = event['message']['text']
                user = event['source']['userId']

                response = get_dify_response(query, user)
                """
                message = client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=msg,
                )

                run = client.beta.threads.runs.create_and_poll(
                    thread_id=thread.id,
                    assistant_id="asst_6F8lxfUAU63nMdxBQrCMPQiM",
                    #instructions="ユーザーを佐藤太郎として扱ってください。ユーザーはプレミアムアカウントを持っています。",
                )

                if run.status == "completed":
                    messages = client.beta.threads.messages.list(thread_id=thread.id)
                    for message in messages.data:
                        if message.role != "user":
                            response += message.content[0].text.value
                """
            elif(event['message']['type'] == "location"):

                latitude = event['message']['latitude']
                longitude = event['message']['longitude']
                address = event['message']['address']
                query = f'今、緯度{latitude}、経度{longitude}の{address}にいます。周辺のおすすめをおしえてください。' + \
                    '出力形式は、場所名は"place",所在地は"address",GoogleMapへのリンクは"gmap", それ以外の説明は"description"に紐づけてjsonで出力してください。 \
                        json形式とは[{"place": "", "address": "", "gmap": "", "description": ""}, {"place": "", "address": "", "gmap": "", "description": ""}]です。'
                user = event['source']['userId']

                response = get_dify_response(query, user)
                print(response)

    except Exception as e: 
        response = f"Error occurred: {str(e)}"

    return response