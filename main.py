# -*- coding: utf-8 -*-
import os
import discord

from dotenv import load_dotenv
load_dotenv()

bot = discord.Bot()


def get_generic_embed():
    out = discord.Embed(title = "**title**", color = 0xffffff)
    out.set_author(name="author")
    out.set_thumbnail(url="https://hololive-official-cardgame.com/wp-content/images/cardlist/hSD03/hSD03-013_C.png") # test okanyan
    out.add_field(name="Field 1", value="Field 1 Value", inline=False)
    out.add_field(name="Field 2 (Inline)", value="Field 2 Value", inline=True)
    return out

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
@bot.slash_command(name="cshow", description="any part of the card name you want to search")
async def cshow(ctx, *, arg):
    search_string = arg
    await ctx.send('search string: "' + search_string + '"')
    embed = get_generic_embed()
    print('sending embed')
    await ctx.respond(embed = embed)
    return

bot.run(os.getenv('TOKEN'))
