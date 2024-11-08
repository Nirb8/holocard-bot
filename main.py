# -*- coding: utf-8 -*-
import discord
import os
import unicodedata
import time
from tabulate import tabulate
from urllib3 import Retry



from dotenv import load_dotenv
load_dotenv()

def to_beautiful_embed(self):
    diveColor = 0xffc800
    if self.type.startswith("Elite Deep Dive") :
        diveColor = 0xb82500
    out = discord.Embed(title = "**{type} | {name}**".format(type = self.type, name=self.name), color = diveColor)
    out.set_author(name=self.biome)
    out.set_thumbnail(url=get_biome_image_embed(self.biome))
    for stage in self.stages:
        if stage[1].startswith("Primary") :
            continue
        stageContents = "**Objectives**: {primary_icon} {primary}** / **{secondary_icon} {secondary}\n**Anomaly**: {anomaly_icon} {anomaly}\n**Warning**: {warning_icon} {warning}".format(primary_icon=get_mission_icon(stage[1]), primary=stage[1], secondary_icon=get_mission_icon(stage[2]), secondary=stage[2],anomaly_icon = get_anomaly_icon(stage[3]), anomaly=stage[3], warning_icon=get_warning_icon(stage[4]), warning=stage[4])
        out.add_field(name="Stage {stg}".format(stg=stage[0]), value=stageContents, inline=False)
    return out

def get_last_deep_dive_info_embed(raw=False):
    submission = get_last_deep_dive_submission()
    if not submission:
        return None
    text = submission.selftext
    if raw:
        return text
    
    dd = parse_deep_dive_info(text, 'Deep Dive')
    edd = parse_deep_dive_info(text, 'Elite Deep Dive')

    if not dd or not edd:
        print('No deep dive (or elite deep dive) info found')
        return None

    url = f'**Source**: <{submission.url}>'
    title = f'**{submission.title}**'

    result = [dd.to_beautiful_embed(), edd.to_beautiful_embed()]

    return result

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


# set as slash command
@client.event
async def on_message(message):
    if any(map(message.content.startswith, "string")):
        info = get_last_deep_dive_info_embed()
        print('sending embed')
        await message.channel.send(get_last_deep_dive_submission().title)
        for embed in info:
            await message.channel.send(embed = embed)
        return


client.run(os.environ['TOKEN'])
