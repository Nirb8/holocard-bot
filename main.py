# -*- coding: utf-8 -*-
import discord
import os
import unicodedata
import time
from tabulate import tabulate
from urllib3 import Retry



from dotenv import load_dotenv
load_dotenv()

def get_generic_embed():
    out = discord.Embed(title = "**title**", color = 0xffffff)
    out.set_author(name="author")
    out.set_thumbnail(url="https://hololive-official-cardgame.com/wp-content/images/cardlist/hSD03/hSD03-013_C.png") # test okanyan
    out.add_field(name="Field 1", value="Field 1 Value", inline=False)
    out.add_field(name="Field 2 (Inline)", value="Field 2 Value", inline=True)
    return out

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# set as slash command later
@client.event
async def on_message(message):
    if any(map(message.content.startswith, "test")):
        embed = get_generic_embed()
        print('sending embed')
        await message.channel.send("Card Title")
        await message.channel.send(embed = embed)
        return

client.run(os.environ['TOKEN'])
