import random
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Load Slack tokens from environment variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# Check if tokens are loaded correctly
if not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN:
    raise ValueError("Missing Slack token. Ensure SLACK_BOT_TOKEN and SLACK_APP_TOKEN are set in the environment.")

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

# List of random insults
INSULTS = [
    "You're as sharp as a marble.",
    "You bring everyone so much joy... when you leave the room.",
    "You're proof that even evolution can take a step back.",
    "You have something on your chin... no, the third one down.",
    "You're like a cloud. When you disappear, it’s a beautiful day."
]

# Define a message handler
@app.message("hello")
def respond_with_insult(message, say, logger):
    # Extract channel ID and user ID from the message
    channel = message.get("channel")
    user = message.get("user")
    
    # Check if the channel is a DM (Slack DMs have channel IDs starting with "D")
    if channel and channel.startswith("D"):
        random_insult = random.choice(INSULTS)
        say(f"<@{user}>, {random_insult}")
    else:
        logger.info("Message received in a non-DM channel, ignoring.")

# Start the app with Socket Mode
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()