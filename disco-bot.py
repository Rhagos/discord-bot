__author__ = 'Domath'

import discord
import asyncio
import time
import datetime
import stock_scraper

client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
    print('Hi there!')
    print('Username: ' + client.user.name)
    print('ID: ' + str(client.user.id))

valid_commands = ['checkperm', 'hello', 'logout', 'nuke', 'clean', 'no', 'oyvey', 'stocks', 'dronestrike']

ENABLE_LOGS = False
@client.event
async def on_message(message):
    keywords = message.content.split(" ")
    if keywords == [] or keywords == None:
        return
    if keywords[0][0] == '-' and keywords[0][1:] not in valid_commands:
        await message.channel.send("Not a valid command, try -help")
    #if not message.author.permissions_in(message.channel).administrator:
    #    await message.channel.send("Wrong door leather man")
    message_permissions = message.author.permissions_in(message.channel).manage_messages
    if message.content.startswith('-'):
        if message.content.startswith('-checkperm'):
            await message.channel.send('Can edit/delete other messages: {0}'.format(message.author.permissions_in(message.channel).manage_messages))

        if message.content.startswith('-hello'):
            await message.channel.send('hello')

        if message.content.startswith('-logout'):
            if message.author.permissions_in(message.channel).administrator:
                await message.channel.send('Powering down...')
                await client.logout()

        if message.content.startswith('-nuke') or message.content.startswith('-dronestrike'):
            if message_permissions:
                if len(keywords) > 1:
                    deleted = await message.channel.purge(limit = min(int(keywords[1]) + 1, 100), check = lambda a: True)
                    if ENABLE_LOGS:
                        with open("Log_nuke_"+str(message.channel)+"_"+str(datetime.datetime.now()), 'w+') as log:
                            for line in deleted:
                                log.write(line.content+"\n")
                    
                else:
                    await message.channel.send('Format is: -clean [number of messages to delete]')
            else:
                await message.channel.send('Does not have proper permissions!')

        if message.content.startswith('-clean'):
            if message_permissions:
                if len(keywords) > 1:
                    not_pinned = lambda x: x.pinned != True
                    deleted = await message.channel.purge(limit = min(int(keywords[1]) + 1, 100), check = not_pinned)
                    if ENABLE_LOGS:
                        with open("Log_clean_"+str(message.channel)+"_"+str(datetime.datetime.now()), 'w+') as log:
                            for line in deleted:
                                log.write(line.content+"\n")
                    
                else:
                    await message.channel.send('Format is: -nuke [number of messages to delete]')
            else:
                    await message.channel.send('Does not have proper permissions!')


        if keywords[0] == '-oyvey' or keywords[0] == '-stocks':
            if keywords[1:] == []:
                await client.send_message(message.channel, "Format is '-stocks <TICKER>'")
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

                        await message.channel.send(breakdown)
                    except Exception as e:
                        await message.channel.send("The fuck? {0}".format(e))

        if keywords[0] == '-help':
            await message.channel.send("Valid commands: {0}".format(valid_commands))

        if keywords[0] == '-no':
            if message_permissions:
                not_pinned = lambda x: x.pinned != True
                history = await message.channel.history().flatten()
                if ENABLE_LOGS:
                    with open("Log_no_"+str(message.channel)+"_"+str(datetime.datetime.now()), 'w+') as log:
                        for no in history:
                            await no.delete()
                            log.write(no.content+"\n")
                else:
                    for no in history:
                        await no.delete()
            else:
                await message.channel.send('Does not have proper permissions!')





key = open("key.scrt", "r").readline()
key = key.strip('\n')
client.run(key, bot = True)
