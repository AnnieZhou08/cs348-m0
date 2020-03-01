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

            if command in [Commands.ListNeighbourhood, Commands.PriceNeighbourHood, Commands.PriceHomestyle]:
                # These 3 commands don't take arguments, just return
                return ParserResponse(command = command)
            elif command == Commands.SuggestHost:
                match = re.match(r"(.*) neighbourhood='(?P<neighbourhood>.*)'(.*)", message)
                if match is None:
                    # match failed or no optional arguments were given
                    return ParserResponse(command = command)
                else:
                    neighbourhood = match.group('neighbourhood')
                    return ParserResponse(command = command, commandArgs = { 'neighbourhood': neighbourhood })
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
                match = re.match(r"(.*) begin='(?P<begin>\d\d\d\d-\d\d-\d\d)' end='(?P<end>\d\d\d\d-\d\d-\d\d)'(.*)", message)
                if match is None:
                    # Command takes mandatory arugments
                    raise ValueError()
                else:
                    begin = match.group('begin')
                    end = match.group('end')
                    return ParserResponse(command = command, commandArgs = { 'begin': begin, 'end': end })
            else:
                raise Exception()


            return ParserResponse(channel, command, None)
