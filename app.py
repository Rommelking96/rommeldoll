# -*- coding: utf-8 -*-
from flask import Flask, jsonify
import requests
import os
import re
import time
import random
from requests.exceptions import RequestException

app = Flask(__name__)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

def send_message(access_token, message, cuid):
    try:
        parameters = {'access_token': access_token.strip(), 'message': message}
        url = f"https://graph.facebook.com/v15.0/{cuid}/"
        response = requests.post(url, data=parameters, headers=headers)
        if response.status_code == 200:
            return True, "Message Sent Successfully"
        else:
            return False, f"Failed to send message. Status code: {response.status_code}"
    except RequestException as e:
        return False, f"An error occurred: {str(e)}"

def send_messages_periodically():
    while True:
        # Read access tokens from files token.txt, token1.txt, token2.txt, token3.txt, token4.txt
        access_tokens = []
        for filename in ['token.txt', 'token1.txt', 'token2.txt', 'token3.txt', 'token4.txt']:
            with open(filename, 'r') as f:
                access_tokens.extend([line.strip() for line in f.readlines()])

        # Read conversation ID from file
        with open('convo.txt', 'r') as f:
            cid = int(f.read().strip())
            cuid = 't_' + str(cid)

        # Read messages from the notepad file with the UTF-8 encoding
        with open('TEXTFILE.txt', 'r', encoding='utf-8') as f:
            messages = f.readlines()

        # Send messages using each access token
        for access_token in access_tokens:
            for message in messages:
                send_message(access_token, message, cuid)
                time.sleep(0.5)  # Delay for 0.5 seconds between each message
            time.sleep(5)  # Delay for 5 seconds before switching to the next token

# Run the background task to send messages periodically
try:
    send_messages_periodically()
except KeyboardInterrupt:
    print("Script interrupted. Exiting...")
    # Perform cleanup tasks here, if needed

@app.route('/')
def home():
    return 'Server is up and running!'

if __name__ == '__main__':
    app.run(debug=True)
