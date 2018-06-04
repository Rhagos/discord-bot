__author__ = 'Domath'

import discord
import asyncio
import time

import stock_scraper

client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    print('Hi there!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)

valid_commands = ['checkperm', 'wipe', 'logout', 'nuke', 'oppress', 'oyvey']


@client.event
@asyncio.coroutine
def on_message(message):
    keywords = message.content.split(" ")
    if keywords == []:
        return
    if keywords[0][1:] not in valid_commands and keywords[0][0] == '-':
        client.send_message("Not a valid command, try -help")
    message_permissions = message.author.permissions_in(message.channel).manage_messages
    if message.content.startswith('-'):
        if message.content.startswith('-checkperm'):
            yield from client.send_message(message.channel, 'Can edit/delete other messages: {0}'.format(message.author.permissions_in(message.channel).manage_messages))

        if message.content.startswith('-wipe'):
            yield from client.send_message(message.channel, 'HELLO WORLD')

        if message.content.startswith('-logout'):
            if message.author.permissions_in(message.channel).manage_server:
                yield from client.send_message(message.channel, 'Powering down...')
                yield from client.logout()

        if message.content.startswith('-nuke'):
            if message_permissions:
                if len(keywords) > 1:
                    not_pinned = lambda x: x.pinned != True
                    deleted = yield from client.purge_from(message.channel, limit = int(keywords[1]) + 1, check = not_pinned)
                else:
                    yield from client.send_message(message.channel,'Format is: !nuke [number of messages to delete]')
            else:
                yield from client.send_message(message.channel, 'Does not have proper permissions!')

        if message.content.startswith('-dronestrike'):
            if message_permissions:
                if len(keywords) > 1:
                    not_pinned = lambda x: x.pinned != True
                    deleted = yield from client.purge_from(message.channel, limit = int(keywords[1]) + 1, check = not_pinned)
                else:
                    yield from client.send_message(message.channel,'Format is: !nuke [number of messages to delete]')
            else:
                yield from client.send_message(message.channel, 'Does not have proper permissions!')

        if message.content.startswith('-oppress'):
            if message_permissions:
                keywords = message.content.split(" ")
                if len(keywords) > 1:
                    messages = yield from client.logs_from(message.channel, int(keywords[1]) + 1)
                    for txt in messages:
                        if not message.pinned:
                            yield from client.delete_message(txt)
                else:
                    yield from client.send_message(message.channel,'Format is: !nuke [number of messages to delete]')
            else:
                yield from client.send_message(message.channel, 'Does not have proper permissions!')
            yield from client.send_message(message.channel, '<:LUL:280188355453648900> Free speech <:LUL:280188355453648900> ')

        if keywords[0] == '-oyvey':
            if keywords[1:] == []:
                yield from client.send_message(message.channel, "SHOO SHOO")
            else:
                for ticker in keywords[1:]:
                    try:
                        data = stock_scraper.parse_page(ticker)
                        print(data)
                        breakdown = "{0} is at {1}, {2} {3} ({4}) from previously.".format(
                                data.get('company_name'),
                                data.get('price'),
                                "DOWN" if float(data.get('change')) < 0 else "UP",
                                data.get('change'),
                                data.get('change_percent'))

                        yield from client.send_message(message.channel, breakdown)
                    except Exception as e:
                        yield from client.send_message(message.channel, "The fuck? {0}".format(e))

        if keywords[0] == '-help':
            yield from client.send_message(message.channel, "Valid commands: {0}".format(valid_commands))



key = open("key.scrt", "r").readline()
key = key.strip('\n')
client.run(key, bot = True)
