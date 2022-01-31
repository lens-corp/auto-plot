import slack
import os
from pathlib import Path
# from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import requests
import pandas as pd
import parsing
import shutil
import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from zipfile import ZipFile
import time
import uploading2
import sys
from univariate_plots import *

env_path = Path('.') / '.env'

# load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app
)
token = os.environ['SLACK_TOKEN']
client = slack.WebClient(token=token)
BOT_ID = client.api_call('auth.test')['user_id']
print(BOT_ID)
# client.chat_postMessage(channel='#test',text='Hey babe')
logger = logging.getLogger(__name__)


f = {}


@slack_event_adapter.on("app_mention")
def message(payload):
    # d=0

    file_name = ''

    client = slack.WebClient(token=token)
    event = payload.get('event', {})
    try:
        user_id = event.get('user')
        msg_time = event.get('event_ts')
        print(msg_time)
        print(time.time())
        msg_gap = (time.time()-float(msg_time))
        print('hihihihhhohohoh', msg_gap)

        channel_id = event.get('channel')
        files = event.get('files')

        if files == None and event.get('bot_id') is None:
            client.chat_postMessage(
                channel=channel_id, text="Hey there! I don't understand any other stuff, Can I interest you in some plots?")
            return

        file_url = files[0]['url_private']
        file_name = files[0]['name']
        r = requests.get(file_url, headers={
                         'Authorization': 'Bearer %s' % token})
        saved_file = 'slack_files/{}'.format(file_name)

        f[saved_file] = msg_gap
        open(saved_file, 'wb').write(r.content)

        if event.get('bot_id') is None and msg_gap < 38:
            data, headers, data_types, filename, d = parsing.get_data(
                saved_file, 1)
            if d != 1:
                client.chat_postMessage(
                    channel=channel_id, text="Hang onto your boots for the results..")
                parsing.start_plotting(data, headers, data_types, filename)
                client.chat_postMessage(
                    channel=channel_id, text="Done Visualizing, Uploading the results.")
                total_images = uploading2.give_output(
                    client, channel_id, event, file_name.split('.')[0])
                if total_images == 0:
                    client.chat_postMessage(
                        channel=channel_id, text="There is nothing to visualize may be because there is empty cell in each row or ")
            elif d == 1:
                client.chat_postMessage(
                    channel=channel_id, text="There is nothing to visualize beacause empty file was shared or the file shared was corrupted.")

            return channel_id

    except Exception as e:
        print(e)
        return


'''
@app.route('/autoplot',methods=['POST','GET'])
def message_count(payload):

    data=request.form
    #print(data)
    user_id=data.get('user_id')
    channel_id=data.get('channel_id')
    message_count=message_counts.get(user_id,0)
    client.chat_postMessage(channel=channel_id, text=f'Message : {message_count}')
    return Response(),200
'''
if __name__ == '__main__':
    app.run(debug=True)
