from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_ASSISTANT_API_KEY"))

def create_single_text_message(event):
    
    response = ""
    thread = client.beta.threads.create()

    try:
        if(event['type'] == "message"):
            if(event['message']['type'] == "text"):

                msg = event['message']['text']
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
        
    except Exception as e: 
        response = f"Error occurred: {str(e)}"

    return response