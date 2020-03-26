from enum import Enum
import logging
import re

class Commands(Enum):
    """
    These are the only valid commands we support.
    """
    Help = 'help'
    ListNeighbourhood = 'list neighbourhood'
    SuggestHost = 'suggest host'
    SuggestDate = 'suggest date'
    PriceDate = 'price date'
    PriceNeighbourHood = 'price neighbourhood'
    PriceHomestyle = 'price homestyle'
    GetListings = 'get listings'
    AddBookmark = 'add bookmark'
    RemoveBookmark = 'remove bookmark'

class ParserResponse:
    """
    Constructor

    Input:
    command         Command             Bot command
    commandArgs     Dictionary          Optional arguments for bot command
    """
    def __init__(self, command, commandArgs = None):
        self.command = command
        self.commandArgs = commandArgs

"""
Returns the group given by argumentName in regexMatch if regexMatch exists

Input:
regexMatch          re.Match            Result of the regex
argumentName        string              Name of the group we want from regexMatch
"""
def argumentOrNone(regexMatch, argumentName):
    return regexMatch.group(argumentName) if regexMatch is not None else None

def intOrNone (x):
    return int(x) if x is not None else None

class Parser:
    """
    Returns a ParserResponse with the parsed command and command arguments

    Raises ValueError on invalid commands

    Input:
    event_message   Dictionary          Dictionary containing the attributes of the slack event
    """
    @staticmethod
    def parse(event_message):
        message = event_message.get('text', '')
        messageWords = message.split(' ')
        if len(messageWords) == 0:
            raise ValueError('Received nothing in message')

        # first word could be the bot id
        if re.match(r'<@.*>', messageWords[0]) is not None:
            messageWords = messageWords[1:]

        # great, we can now have an empty command again
        # let's be helpful and assume that the user means to type the help command
        if len(messageWords) == 0:
            return ParserResponse(command = Commands.Help)

        # now we try to match the command
        if messageWords[0] == 'help':
            # help is the only one word command
            return ParserResponse(command = Commands.Help)
        else:
            # the remaining commands are all two words long
            if len(messageWords) < 2:
                raise ValueError('Invalid Command')

            mCommand = ' '.join(messageWords[0:2])
            command = Commands(mCommand) # This may raise an exception

            if command in [Commands.ListNeighbourhood, Commands.PriceHomestyle]:
                # These 3 commands don't take arguments, just return
                return ParserResponse(command = command)
            elif command == Commands.PriceNeighbourHood:
                match = re.match(r"(.*)price neighbourhood '(?P<neighbourhood>.*)'", message)
                if match is None:
                    return ParserResponse(command = command)
                else:
                    neighbourhood = match.group('neighbourhood')
                    return ParserResponse(command = command, commandArgs = { 'neighbourhood': neighbourhood })
            elif command == Commands.SuggestHost:
                neighbourhood = re.match(r"(.*)neighbourhood='(?P<neighbourhood>.*)'(.*)", message)
                numberOf = re.match(r"(.*)numberOf=(?P<numberOf>\d+)(.*)", message)
                neighbourhood = neighbourhood.group('neighbourhood') if neighbourhood is not None else None
                numberOf = int(numberOf.group('numberOf')) if numberOf is not None else None

                return ParserResponse(command = command, commandArgs = { 'neighbourhood': neighbourhood, 'numberOf': numberOf })
            elif command == Commands.SuggestDate:
                match = re.match(r"(.*) begin='(?P<begin>\d\d\d\d-\d\d-\d\d)' end='(?P<end>\d\d\d\d-\d\d-\d\d)'(.*)", message)
                if match is None:
                    # match failed or no optional arguments were given
                    return ParserResponse(command = command)
                else:
                    begin = match.group('begin')
                    end = match.group('end')
                    return ParserResponse(command = command, commandArgs = { 'begin': begin, 'end': end })
            elif command == Commands.PriceDate:
                match = re.match(r"(.*) begin='(?P<begin>\d\d\d\d-\d\d-\d\d)' end='(?P<end>\d\d\d\d-\d\d-\d\d)' neighbourhood='(?P<neighbourhood>.*)'(.*)", message)
                if match is None:
                    match = re.match(r"(.*) begin='(?P<begin>\d\d\d\d-\d\d-\d\d)' end='(?P<end>\d\d\d\d-\d\d-\d\d)'(.*)", message)
                    if match is None:
                        # Command takes mandatory arugments
                        raise ValueError()
                    else:
                        begin = match.group('begin')
                        end = match.group('end')
                        return ParserResponse(command = command, commandArgs = { 'begin': begin, 'end': end })
                else:
                    begin = match.group('begin')
                    end = match.group('end')
                    neighbourhood = match.group('neighbourhood')
                    return ParserResponse(command = command, commandArgs = { 'begin': begin, 'end': end, 'neighbourhood': neighbourhood })
            elif command == Commands.GetListings:
                host = argumentOrNone(re.match(r"(.*)host='(?P<host>.*?)'(.*)", message), 'host')
                neighbourhood = argumentOrNone(re.match(r"(.*)neighbourhood='(?P<neighbourhood>.*?)'(.*)", message), 'neighbourhood')

                numPeople = intOrNone(argumentOrNone(re.match(r"(.*)numPeople=(?P<numPeople>\d+)(.*)", message), 'numPeople'))
                startPrice = intOrNone(argumentOrNone(re.match(r"(.*)startPrice=(?P<startPrice>\d+)(.*)", message), 'startPrice'))
                endPrice = intOrNone(argumentOrNone(re.match(r"(.*)endPrice=(?P<endPrice>\d+)(.*)", message), 'endPrice'))
                numResults = intOrNone(argumentOrNone(re.match(r"(.*)numResults=(?P<numResults>\d+)(.*)", message), 'numResults'))

                return ParserResponse(
                    command = command,
                    commandArgs = {
                        'host': host,
                        'neighbourhood': neighbourhood,
                        'numPeople': numPeople,
                        'startPrice': startPrice,
                        'endPrice': endPrice,
                        'numResults': numResults
                    }
                )
            elif command == Commands.AddBookmark:
                slack_user_id = event_message.get('user', '')
                listing_id = intOrNone(argumentOrNone(re.match(r"(.*)listingID=(?P<listingID>\d+)(.*)", message), 'listingID'))
                return ParserResponse(
                    command = command,
                    commandArgs = {
                        'slackUserID': slack_user_id,
                        'listingID': listing_id,
                    }
                )
            elif command == Commands.RemoveBookmark:
                slack_user_id = event_message.get('user', '')
                listing_id = intOrNone(argumentOrNone(re.match(r"(.*)listingID=(?P<listingID>\d+)(.*)", message), 'listingID'))
                print("HI")
                print(message)
                return ParserResponse(
                    command = command,
                    commandArgs = {
                        'slackUserID': slack_user_id,
                        'listingID': listing_id,
                    }
                )
            else:
                raise Exception()


            return ParserResponse(channel, command, None)
