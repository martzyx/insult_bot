import random
import json
import os
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

print(f"Current working directory: {os.getcwd()}")

# Load Slack tokens from environment variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# Check if tokens are loaded correctly
if not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN:
    raise ValueError("Missing Slack token. Ensure SLACK_BOT_TOKEN and SLACK_APP_TOKEN are set in the environment.")

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

# List of quotes
quotes = [
    "yeah, don't worry about it.",
    "them boys been making salad...",
    "is it gonna fail? Probably.",
    "why are you asking me? I just work here.",
    "we don't follow guides, we do things... differently.",
    "oh boy...",
    "I like to call this \"faith based programming\"",
    "will it work? Probably not. Are wj proud? Hell yeah.",
    "are you driving value today?",
    "I hate clerk.js...",
    "are you using a GUI? Ew.",
    "have you heard of Vim?",
    "if you're not using Vim, I have lost my respect for you",
    "you're a good guy, okay?",
    "in case of failure, always examine someone else's execution.",
    "i am calling in sick tomorrow.",
    "AI is wrong",
    "buy low, sell high",
    "focus on your non-constructive criticism",
    "one of the best ways to beat the market is to pick the right stock",
    "you can guarantee success, by consistently lowering your standards",
    "never doubt yourself, if you can doubt someone else",
    "people ask me how to succeed. simple, avoid failure",
    "work harder, not smarter."
]

# File to store usage count and user data
DATA_FILE = "/app/data/user_usage.json"

# Load user usage data from file
def load_user_data():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("File not found. Initializing user data to an empty dictionary.")
        return {}
    except Exception as e:
        print(f"Error loading user data: {e}")
        return {}

# Save user usage data to file
def save_user_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Error saving user data: {e}")

# Initialize user data
user_data = load_user_data()

# Define a message handler
@app.message(re.compile(r"\b(hello|hi|hey)\b", re.IGNORECASE))
def respond_with_quote(message, say, logger):
    global user_data

    # Extract channel ID and user ID from the message
    channel = message.get("channel")
    user_id = message.get("user")
    user_info = app.client.users_info(user=user_id)
    username = user_info["user"]["name"]

    # Increment the interaction count for the user
    user_data[username] = user_data.get(username, 0) + 1
    save_user_data(user_data)

    # Check if the channel is a DM (Slack DMs have channel IDs starting with "D")
    if channel and channel.startswith("D"):
        random_quote = random.choice(quotes)
        say(f"<@{user_id}>, {random_quote}")
        logger.info(f"{username} has interacted with the bot {user_data[username]} times.")
    else:
        logger.info("Message received in a non-DM channel, ignoring.")

# Start the app with Socket Mode
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
