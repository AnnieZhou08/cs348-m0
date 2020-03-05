from django.shortcuts import render
import json
import logging

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import slack

# Queries
from queries.get_listings import get_listings
from queries.list_neighborhoods import get_neighborhoods
from queries.price_neighborhoods import get_neighborhood_price

# Parsing
from module.parser import Parser, ParserResponse, Commands

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
            return Response(data=slack_message, status=status.HTTP_200_OK)

	# greet bot
        if 'event' in slack_message:
            event_message = slack_message.get('event')
            channel = event_message.get('channel')
            print('Event Message', event_message)


            if 'bot_id' in event_message or 'bot_profile' in  event_message:
                # Just return a response code if we see our own message
                return Response(status = status.HTTP_200_OK)

            # ----------------------------------------------------
            # What does this code do?
            # if event_message.get('sub_type') == 'bot_message':
            #     return Response(status=status.HTTP_200_OK)
            #
            # if event_message.get('type') == 'app_mention':
            #     channel = event_message.get('channel')
            #     price = get_neighborhood_price("")
            #     Client.chat_postMessage(channel=channel, text=price)
            #     return Response(status=status.HTTP_200_OK)
            # ----------------------------------------------------

            try:
                parse_result = Parser.parse(event_message)
                command = parse_result.command
                commandArgs = parse_result.commandArgs

                # These are stubs, replace the "text=" part with calls to the
                # actual queries
                if command == Commands.Help:
                    Client.chat_postMessage(
                        channel = channel,
                        text = (
                            "Commands:\n"
                            "`help` - Prints this!\n"
                            "\n`list neighbourhood` - Returns a list of neighbourhoods\n"
                            "\n`suggest host <neighbourhood=''>` - Returns suggested hosts\n"
                            "Usage:\n"
                            "- `suggest host`:\n"
                            "- `suggest host neighbourhood='downtown'`:\n"
                            "\n`suggest date <begin='' end=''>` - Returns suggested dates\n"
                            "Usage:\n"
                            "- `suggest date`:\n"
                            "- `suggest date begin='2018-07-01' end='2018-08-01'`:\n"
                            "\n`price date begin='' end='' <neighbourhood=''>` - Returns the average price within the date range (and optionally for one neighbourhood)\n"
                            "Usage:\n"
                            "- `price date begin='2018-07-01' end='2018-08-01'`:\n"
                            "- `price date begin='2018-07-01' end='2018-08-01' neighbourhood='downtown'`:\n"
                            "\n`price neighbourhood <neighbourhood>` - Returns the average price in different neighbourhoods (or optionally, from one neighbourhood)\n"
                            "Usage:\n"
                            "- `price neighbourhood`"
                            "- `price neighbourhood 'downtown'`\n"
                            "\n`price homestyle` - Returns the average price for different homestyles\n"
                        )
                    )
                elif command == Commands.ListNeighbourhood:
                    Client.chat_postMessage(
                        channel = channel,
                        text = get_neighborhoods()
                    )
                elif command == Commands.SuggestHost:
                    Client.chat_postMessage(
                        channel = channel,
                        text = '{}, {}'.format(command, commandArgs)
                    )
                elif command == Commands.SuggestDate:
                    Client.chat_postMessage(
                        channel = channel,
                        text = '{}, {}'.format(command, commandArgs)
                    )
                elif command == Commands.PriceDate:
                    Client.chat_postMessage(
                        channel = channel,
                        text = '{}, {}'.format(command, commandArgs)
                    )
                elif command == Commands.PriceNeighbourHood:
                    neighbourhood = commandArgs['neighbourhood'] if (commandArgs is not None and 'neighbourhood' in commandArgs) else ''
                    Client.chat_postMessage(
                        channel = channel,
                        text = get_neighborhood_price(neighbourhood)
                    )
                elif command == Commands.PriceHomestyle:
                    Client.chat_postMessage(
                        channel = channel,
                        text = '{}, {}'.format(command, commandArgs)
                    )
                else:
                    logging.error('Invalid Command: {}\nSlack Message: {}'.format(command, slack_message))
            except ValueError as e:
                logging.error(e)
                if channel is not None:
                    Client.chat_postMessage(
                        channel = channel,
                        text = ":cry: Sorry, I don't understand that commmand. Perhaps try `help`?"
                    )
            except Exception as e:
                logging.error(e)
                logging.error('Parse failed on slack message: {}'.format(slack_message))



        return Response(status=status.HTTP_200_OK)
