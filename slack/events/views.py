from django.shortcuts import render
import json

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slackclient import SlackClient

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings,                          #2
'SLACK_BOT_USER_TOKEN', None)                                     #
Client = SlackClient(SLACK_BOT_USER_TOKEN)                        #3

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
                Client.api_call(method='chat.postMessage',
                                        channel=channel,
                                        text="hello")
                return Response(status=status.HTTP_200_OK)


        return Response(status=status.HTTP_200_OK)

