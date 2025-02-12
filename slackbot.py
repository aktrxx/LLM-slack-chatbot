import os
# import openai
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from collections import deque
from deepseek_LLM_server import *


SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)

message_history = {}

@app.event("app_mention")
def handle_mention(event, say):
    print("Event log")
    channel_id = event["channel"]
    user_query = event["text"]
    thread_ts = event.get("thread_ts", event["ts"]) 

    if channel_id not in message_history:
        message_history[channel_id] = deque(maxlen=5)
    

    message_history[channel_id].append(user_query)

    context_messages = list(message_history[channel_id])
    
    
    reply_text = llm_chatbot(user_query)
    

    say(text=reply_text)
    # say(text=reply_text)


# Start the app
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
