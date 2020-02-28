from django.shortcuts import render
import json
import queries.list_neighborhoods as ln

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import slack
from queries.get_listings import get_listings

import pymysql
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='passw0rd',
                             db='cs348m0')

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings,                          #2
'SLACK_BOT_USER_TOKEN', None)                                     #
Client = slack.WebClient(SLACK_BOT_USER_TOKEN)                        #3

class Events(APIView):
    def post(self, request, *args, **kwargs):
        slack_message = request.data
        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

	# verification challenge
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message,
                            status=status.HTTP_200_OK)

	# greet bot
        if 'event' in slack_message:
            event_message = slack_message.get('event')
            channel = event_message.get('channel')
            
            if event_message.get('sub_type') == 'bot_message':
                return Response(status=status.HTTP_200_OK)
            
            if event_message.get('type') == 'app_mention':
                channel = event_message.get('channel')
                all_neighbourhoods = get_listings(connection, "Noe Valley")
                Client.chat_postMessage(channel=channel,
                                   text=all_neighbourhoods)
                return Response(status=status.HTTP_200_OK)


        return Response(status=status.HTTP_200_OK)

