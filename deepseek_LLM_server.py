import requests
import json
import re

llm_host = 'http://localhost:11434/api/generate'

LLM_MODEL = "deepseek-r1:listenToAktrxx"

def llm_chatbot(prompt):

    payload = {
    'model': LLM_MODEL,
    "prompt": prompt,
    }

    response = requests.post(llm_host, json=payload, stream=True)

    chat_response = ''
    if response.status_code==200:
        print("Generated text", end=' ', flush=True)
        for line in response.iter_lines():
            if line:
                decode_line = line.decode('utf-8')
                result = json.loads(decode_line)
                generated_text = result.get("response", "")
                chat_response += generated_text
                print("\rThinking...", end='', flush=True)
        print(chat_response)

        cleaned_text = re.sub(r'<think>.*?</think>\s*', '', chat_response, flags=re.DOTALL)

        return cleaned_text
    else:
        print('Error')
        return "Error"

if __name__ == "__main__":
    llm_chatbot('Hi hello')