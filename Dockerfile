# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install the Python dependencies
RUN pip install --no-cache-dir slack-bolt

# # Set environment variables (or load from a file later)
# ENV SLACK_BOT_TOKEN=your-bot-token
# ENV SLACK_APP_TOKEN=your-app-token

# Run the Python script
CMD ["python", "insult_bot.py"]