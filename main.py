# -*- coding: utf-8 -*-
import os
import re
import discord
import json
from card_dropdown import CardDropdown

from dotenv import load_dotenv

from embeds import get_embed_for_card
from emoji_utils import get_quick_info_string
load_dotenv()

bot = discord.Bot()

holomen_dict = {}
support_dict = {}
oshi_dict = {}

def strip_whitespace_brackets_and_quotes_and_lowercase(str):
    return re.sub(r'(\]|\[|:|\\|,|{|}|\"|\s|\u180B|\u200B|\u200C|\u200D|\u2060|\uFEFF)+', '', str).lower()


def load_json():
    # Open the JSON file and read its contents
    with open('data.json', 'r') as file:
        data = json.load(file)

    for card_id, card in data.items():
        card_type = card.get('type')
        if card_type == 'ホロメン' or 'buzz' in card_type.lower():
            holomen_dict[card_id] = card
        elif card_type.startswith('サポート'):
            support_dict[card_id] = card
        elif card_type == '推しホロメン':
            oshi_dict[card_id] = card
    return data

card_dict = load_json()

# TODO: THIS IS A TEST METHOD, REMOVE
def get_generic_embed():
    out = discord.Embed(title = "**title**", color = 0xffffff)
    out.set_author(name="author")
    out.set_thumbnail(url="https://hololive-official-cardgame.com/wp-content/images/cardlist/hSD03/hSD03-013_C.png") # test okanyan
    out.add_field(name="Field 1", value="Field 1 Value", inline=False)
    out.add_field(name="Field 2 (Inline)", value="Field 2 Value", inline=True)
    return out

# TODO: THIS IS A TEST METHOD, REMOVE
def get_full_image_embed():
    out = discord.Embed(image="https://hololive-official-cardgame.com/wp-content/images/cardlist/hSD03/hSD03-013_C.png",
                        title="title",
                        description="description")
    return out

# TODO: THIS IS A TEST METHOD, REMOVE
def find_top_cards(to_search):
    results = {}
    for card in card_dict.values():
        card_id = card["id"].lower()
        for search_str in to_search:
            # print(card["search_string"])
            if(card["search_string"].lower().find(search_str.lower()) >= 0):
                if (card_id in results):
                    results[card_id] += 1
                else:
                    results[card_id] = 1
    return results

def fuzzy_match(search_term, target):
    search_term = search_term.lower()
    target = target.lower()
    matches = sum(1 for a, b in zip(search_term, target) if a == b)
    return matches / max(len(search_term), len(target)) > 0.6

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
@bot.slash_command(name="cshow", description="any part of the card name you want to search")
async def cshow(ctx, *, arg):
    search_strings = arg.split(" ")
    search_strings_debug = ''
    for str in search_strings:
        search_strings_debug += f'{str}, '
    search_strings_debug = search_strings_debug.rstrip(',')
    await ctx.send(f'searcsh strings: {search_strings_debug}')
    embed = get_generic_embed()
    print('sending embed')
    await ctx.respond(embed = embed)
    await ctx.send(embed = get_full_image_embed())
    return

@bot.slash_command(name="cshowid", description="debug command: search card directly by ID")
async def cshowid(ctx, arg):
    search_id = arg
    embed = get_embed_for_card(card_dict[search_id], False)
    await ctx.respond(embed = embed)

@bot.slash_command(name="cshowidfull", description="debug command: search card directly by ID. Also uses full image embed instead of thumbnail")
async def cshowidfull(ctx, arg):
    search_id = arg
    embed = get_embed_for_card(card_dict[search_id], True)
    await ctx.respond(embed = embed)


async def create_multiple_results_embed(ctx, results):
    desc = [get_quick_info_string(card, verbose=True) for card in results]
    card_info = ""
    card_index = 1
    for card in desc:
        card_info += f"{card_index}. {card} \n"
        card_index += 1
    embed = discord.Embed(title="Results", description=card_info)

    dropdown = CardDropdown(results)
    view = discord.ui.View()
    view.add_item(dropdown)
    await ctx.respond("Multiple results found. Please select a card:", embed=embed, view=view, ephemeral=True)


@bot.slash_command(name="holomen", description="search holomen card directly by Bloom lvl, Name, HP. Supports Japanese or English translations.")
async def show_holomen(ctx, arg):
    args = arg.split(" ")
    search_bloom_level = args[0]
    search_name = args[1]
    search_hp = args[2] if len(args) > 2 else None

    # Currently handles the case where translated_content_en is missing; eventually this can be removed
    # TODO: temp disabled fuzzy match, reenable when fixed
    results = [
        card for card in holomen_dict.values()
        if (search_bloom_level.lower() in card["bloom_level"].lower() and
            search_name in card["alias"] and
            (search_hp is None or search_hp.lower() in card["hp"].lower()))
    ]

    await ctx.respond(f"Found {len(results)} results: {[card['id'] for card in results]}")

    if not results:
        await ctx.respond("No results found.")
        return
    elif len(results) == 1:
        embed = get_embed_for_card(results[0], True)
        await ctx.respond(embed=embed)
    # handle multiple results
    else:
        await create_multiple_results_embed(ctx, results)


@bot.slash_command(name="support", description="search support card directly by Name. Supports Japanese or English translations.")
async def show_support(ctx, arg):
    search_name = strip_whitespace_brackets_and_quotes_and_lowercase(arg.lower())
    results = [
        card for card in support_dict.values()
        if search_name in card["alias"]
    ]

    await ctx.respond(f"Found {len(results)} results: {[card['id'] + card['name'] for card in results]}")

    if not results:
        await ctx.respond("No results found.")
        return
    elif len(results) == 1:
        embed = get_embed_for_card(results[0], True)
        await ctx.respond(embed=embed)
    else:
       await create_multiple_results_embed(ctx, results)


@bot.slash_command(name="oshi-holomen", description="search oshi-holomen card directly by Name. Supports Japanese or English translations.")
async def show_oshi_holomen(ctx, arg):
    args = arg.split(" ")
    search_name = args[0]

    results = [
        card for card in oshi_dict.values()
        if (fuzzy_match(search_name, card.get("translated_content_en", {}).get("name", "")))
    ]

    await ctx.respond(f"Found {len(results)} results: {[card['id'] for card in results]}")

    if not results:
        await ctx.respond("No results found.")
        return
    elif len(results) == 1:
        embed = get_embed_for_card(results[0], True)
        await ctx.respond(embed=embed)
    else:
        await create_multiple_results_embed(ctx, results)

bot.run(os.getenv('TOKEN'))

