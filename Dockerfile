# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

FROM python:3.10.8-slim-buster

# System updates and install git
RUN apt update && apt upgrade -y && apt install -y git

# Install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r /requirements.txt

# Set working directory
WORKDIR /FileToLink
COPY . /FileToLink

# Start the bot
CMD ["python3", "bot.py"]
