import slack
import os
from pathlib import Path
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import requests
import pandas as pd
import parser
import shutil
import logging
import glob
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from zipfile import ZipFile
import time


def inc(t):
    return t+1


def give_output(client, channel_id, event, filename):

    folders = ['Univariate_Plots', 'Bivariate_Plots', 'Misc_Plots']

    total_images = 0
    for i in folders:

        folder_name = 'saved_plots/'+filename+'_'+i
        img_files = glob.glob(folder_name + "/**/*.png", recursive=True)

        total_images += len(img_files)

    if total_images == 0:
        return total_images

    else:
        client.chat_postMessage(
            channel=channel_id,
            blocks=[
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Univariate plots",
                                "emoji": True
                            }
                },
                {
                    "type": "section",
                            "fields": [
                                {
                                    "type": "plain_text",
                                    "text": "◙ Box plots",
                                    "emoji": True
                                },
                                {
                                    "type": "plain_text",
                                    "text": "◙ Histograms ",
                                    "emoji": True
                                },
                                {
                                    "type": "plain_text",
                                    "text": "◙ Countplots",
                                    "emoji": True
                                },
                                {
                                    "type": "plain_text",
                                    "text": "◙ Distplots",
                                    "emoji": True
                                }
                            ]
                }
            ]
        )

        folder_name = 'saved_plots/'+filename+'_Univariate_Plots'
        zipnames = 'saved_plots/'+filename+'_Univariate_Plots'
        result = client.files_upload(
            channels=channel_id,
            file='{}.zip'.format(zipnames),
        )

        client.chat_postMessage(
            channel=channel_id,
            blocks=[
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "Bivariate plots",
                                "emoji": True
                            }
                },
                {
                    "type": "section",
                            "fields": [
                                {
                                    "type": "plain_text",
                                    "text": "◙ Scatter 2d plots",
                                    "emoji": True
                                },
                                {
                                    "type": "plain_text",
                                    "text": "◙ Line 2d plots",
                                    "emoji": True
                                }
                            ]
                }
            ]
        )

        folder_name = 'saved_plots/'+filename+'_Bivariate_Plots'
        zipnames = 'saved_plots/'+filename+'_Bivariate_Plots'
        result = client.files_upload(
            channels=channel_id,
            file='{}.zip'.format(zipnames),
        )

        client.chat_postMessage(
            channel=channel_id,
            blocks=[
                {
                    "type": "divider"
                },
                {
                    "type": "header",
                    "text": {
                            "type": "plain_text",
                        "text": "Miscellaneous plots",
                                "emoji": True
                    }
                },
                {
                    "type": "section",
                    "fields": [
                            {
                                "type": "plain_text",
                                "text": "◙ Scatter 3d plots",
                                "emoji": True
                            },
                        {
                                "type": "plain_text",
                                "text": "◙ Groupby plots",
                                "emoji": True
                            }
                    ]
                }
            ]
        )

        folder_name = 'saved_plots/'+filename+'_Misc_Plots'
        zipnames = 'saved_plots/'+filename+'_Misc_Plots'
        result = client.files_upload(
            channels=channel_id,
            file='{}.zip'.format(zipnames),
        )

        return total_images
