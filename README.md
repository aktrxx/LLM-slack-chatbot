# Ana - Slack AI Chatbot

Ana is an AI-powered chatbot integrated with Slack, leveraging DeepSeek LLM for intelligent responses. It maintains context using the last 5 messages via a deque data structure.

## Prerequisites

### 1. Install Ollama and Run DeepSeek LLM

1. Install Ollama on your system: [Ollama Installation Guide](https://ollama.ai/)
2. Run DeepSeek LLM (choose the latest version compatible with your system):
   ```sh
   ollama run deepseek-r1
   ```

### 2. Install Required Python Packages

```sh
pip install slack-bolt slack-sdk requests ollama
```

### 3. Create Your Custom Model

Run `LLM-Deepseek-R1_config.ipynb` to create a custom LLM model:
```python
ollama.create(
  model="deepseek-r1:YourModelName",
  from_="deepseek-r1:1.5b",
  system="Your custom chatbot instructions...",
  parameters={"max_tokens": 500},
)
```

### 4. Create a Slack Bot

1. Go to [Slack API](https://api.slack.com/apps)
2. Click **Create New App** → **From Scratch**
3. Add **Bot User** & **Permissions**:
   - `app_mentions:read`
   - `channels:history`
   - `chat:write`
   - `groups:history`
   - `im:history`
   - `commands`
4. Enable **Socket Mode** & **Event Subscriptions**
5. Copy **SLACK_BOT_TOKEN** and **SLACK_APP_TOKEN**

### 5. Configure Environment Variables

Create a `.env` file with your Slack credentials:
```sh
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
```

## Running the Chatbot

```sh
python slackbot.py
```

## Code Explanation

### **1. `slackbot.py`**
- Initializes the Slack bot (`slack-bolt`).
- Stores the last 5 messages using `deque`.
- Sends user queries to the LLM (`deepseek-r1`).
- Replies in the same Slack thread.

### **2. `deepseek_LLM_server.py`**
- Calls DeepSeek LLM via `ollama.chat()`.
- Cleans responses before sending them back.

### **3. `LLM-Deepseek-R1_config.ipynb`**
- Configures the chatbot model (`ollama.create()`).

## How the Chatbot Works

1. Listens for mentions in Slack (`@Ana`).
2. Stores messages using `deque(maxlen=5)` to maintain context.
3. Sends context + user query to DeepSeek LLM.
4. Receives a response and replies in Slack.

## Example

**User:** `@Ana What is Doctor Droid?`  
**Ana:** `Doctor Droid is a company based in Bengaluru, India, founded by Siddarth Jain and Dipesh Mittal.`

---

Developed by Shakeel Akthar 🚀
