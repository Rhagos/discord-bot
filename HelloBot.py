__author__ = 'Domath'

import discord
import asyncio
import time
client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    print('Hi there!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)

valid-commands = ['checkperm', 'wipe', 'logout', 'nuke', 'oppress', 'oyvey']


@client.event
@asyncio.coroutine
def on_message(message):
    keywords = message.content.split(" ")
    if keywords[0][1:] not in valid-commands && keywords[0][0] == '-':
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
                #ADD SCRAPING STOCK DATA HERE



client.run('MjYwNjM4MTUwNTIxNTIwMTMx.CzpRtQ.i-Hw9RJ7DFBzD0ABZDqbihzkNjs')
