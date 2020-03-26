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
from queries.avg_price import avg_price, avg_price_per_style
from queries.suggest_hosts import suggest_hosts
from queries.bookmark import add_bookmark, remove_bookmark, list_bookmark
from queries.list_popular_listings import get_pop_listings

# Parsing
from module.parser import Parser, ParserResponse, Commands
from module.db_connection import Connection

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
        conn = Connection.get_db_conn()
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


            if 'bot_id' in event_message or 'bot_profile' in event_message or 'subtype' in event_message:
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
                            "*Help*: `help`\n"
                            "\n\n*List neighbourhoods*: `list neighbourhood`\n"
                            "\n\n*Suggest hosts*: `suggest host <neighbourhood=''> <numberOf=''>` (Optionally supply a neighbourhood or restrict the number of results)\n"
                            "Usage:\n"
                            "- `suggest host`\n"
                            "- `suggest host neighbourhood='downtown'`\n"
                            "- `suggest host numberOf=5`\n"
                            "- `suggest host neighbourhood='downtown' numberOf=5`\n"
                            "\n\n*Suggest dates*: `suggest date <begin='' end=''>`\n"
                            "Usage:\n"
                            "- `suggest date`\n"
                            "- `suggest date begin='2018-07-01' end='2018-08-01'`\n"
                            "\n\n*Search average price given dates*: `price date begin='' end='' <neighbourhood=''>` (Optionally supply a neighbourhood)\n"
                            "Usage:\n"
                            "- `price date begin='2018-07-01' end='2018-08-01'`\n"
                            "- `price date begin='2018-07-01' end='2018-08-01' neighbourhood='downtown'`\n"
                            "\n\n*Search average price given neighbourhood*: `price neighbourhood <neighbourhood>` (Optionally restrict results to one neighbourhood)\n"
                            "Usage:\n"
                            "- `price neighbourhood`\n"
                            "- `price neighbourhood 'downtown'`\n"
                            "\n\n*Search average price given homestyle*: `price homestyle`\n"
                            "\n\n*Get list of Listings*: `get listings <neighbourhood, host, numPeople, startPrice, endPrice, numResults>` (All parameters optional)\n"
                            "Usage:\n"
                            "- `get listings neighbourhood='downtown' numPeople=3 endPrice=10000 startPrice=10`\n"
                            "\n\n*Add Bookmark*: `add bookmark <listingID=''> <comment=''>` (Optionally add a comment)\n"
                            "Usage:\n"
                            "- `add bookmark listingID=42`\n"
                            "- `add bookmark listingID=42 comment='this listing is great!'`\n"
                            "\n\n*Remove Bookmark*: `remove bookmark <listingID=''>` (Optionally supply a listingID)\n"
                            "Usage:\n"
                            "- `remove bookmark` (Removes all bookmarks)\n"
                            "- `remove bookmark listingID=42`\n"
                            "\n\n*List Bookmarks*: `list bookmark`\n"
                            "\n\n*Get list of popular listings*: `popular listings <numResults>` (Optionally restrict number of results)\n"
                            "Usage:\n"
                            "- `popular listings`\n"
                            "- `popular listings 25`\n"
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
                        text = suggest_hosts(commandArgs['neighbourhood'], commandArgs['numberOf'])
                    )
                elif command == Commands.SuggestDate:
                    Client.chat_postMessage(
                        channel = channel,
                        text = '{}, {}'.format(command, commandArgs)
                    )
                elif command == Commands.PriceDate:
                    neighbourhood = commandArgs['neighbourhood'] if (commandArgs is not None and 'neighbourhood' in commandArgs) else ''
                    Client.chat_postMessage(
                        channel = channel,
                        text = avg_price(connection,
                                         neighbourhood,
                                         commandArgs['begin'],
                                         commandArgs['end'])
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
                        text = avg_price_per_style(connection)
                    )
                elif command == Commands.GetListings:
                    Client.chat_postMessage(
                        channel = channel,
                        text = get_listings(
                            host = commandArgs['host'],
                            nbrhd = commandArgs['neighbourhood'],
                            numPeople = commandArgs['numPeople'],
                            startPrice = commandArgs['startPrice'],
                            endPrice = commandArgs['endPrice'],
                            numResults = commandArgs['numResults']
                        )
                    )
                elif command == Commands.AddBookmark:
                    Client.chat_postMessage(
                        channel = channel,
                        text = add_bookmark(
                            conn = connection,
                            slack_user_id = commandArgs['slackUserID'],
                            listing_id = commandArgs['listingID'],
                            comments=commandArgs['comment']
                        )
                    )
                elif command == Commands.RemoveBookmark:
                    Client.chat_postMessage(
                        channel = channel,
                        text = remove_bookmark(
                            conn = connection,
                            slack_user_id = commandArgs['slackUserID'],
                            listing_id = commandArgs['listingID']
                        )
                    )
                elif command == Commands.ListBookmark:
                    Client.chat_postMessage(
                        channel = channel,
                        text = list_bookmark(
                            conn = connection,
                            slack_user_id = commandArgs['slackUserID'],
                        )
                    )
                elif command == Commands.PopularListings:
                    Client.chat_postMessage(
                        channel = channel,
                        text = get_pop_listings(commandArgs['numResults'])
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
