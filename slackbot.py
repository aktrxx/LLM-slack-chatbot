import os
# import openai
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from collections import deque
from deepseek_LLM_server import *


SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SYSTEM_BASE_BEHAVIOUR = "You are the chatbot agent named 'Ana' in a company named 'Doctor Droid', your job is to give answers to the questions about the company in the slack channel, every inputs comes to you is from Slack msg, respond to them accordingly, Note down the fllowing information about the company, your answers shoudl be based on the following. Company Name: Doctor Droid, Company Location: Bengaluru, India. Company founders are Siddarth Jain and Dipesh Mittal. you called by your username, help the user who asking questions, Answer withing two or three sentence, dont give long answers more than 600 characters"

app = App(token=SLACK_BOT_TOKEN)
client = WebClient(token=SLACK_BOT_TOKEN)

message_history = {}


def get_user_name(user_id):
    user_info = client.users_info(user=user_id)
    return user_info["user"]["real_name"]



def process_query(thread_ts, sender_name, user_query  ):
    if thread_ts not in message_history:
        message_history[thread_ts] = deque(maxlen=5)
        # message_history[thread_ts] .append({"role": "system", "content": "You are a helpful assistant"})
    
    message_history[thread_ts].append({"role": "user", "content": user_query})

    context_messages = list(message_history[thread_ts])

    # print(context_messages)
    context_messages.insert(0, {"role": "system", "content": SYSTEM_BASE_BEHAVIOUR})
    reply_text = llm_deepseek(context_messages)
    message_history[thread_ts].append({"role": "assistant", "content": reply_text})
    
    # print("Message History:")
    # print()
    # print(message_history)
    # print()

    
    return reply_text



@app.event("app_mention")
def handle_mention(event, say):
    channel_id = event["channel"]
    user_query = event["text"]
    thread_ts = event.get("thread_ts", event["ts"]) 

    sender_name = get_user_name(event["user"])

    reply_text = process_query(thread_ts, sender_name, user_query)

    say(text=reply_text, thread_ts=thread_ts)



if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
