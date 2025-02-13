import re
import ollama


LLM_MODEL = "deepseek-r1:listenToAktrxx"

def llm_deepseek(prompt):

    # print("prompt")
    # print()
    # print(prompt)
    # print()

    chat_res = ollama.chat(
        model=LLM_MODEL,
        messages= prompt
        )
    cleaned_text = re.sub(r'<think>.*?</think>\s*', '', chat_res['message']['content'], flags=re.DOTALL)
    return cleaned_text

if __name__ == "__main__":
    llm_deepseek("Hi, what is your name?")