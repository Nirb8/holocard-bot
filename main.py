# -*- coding: utf-8 -*-
import os
import discord
import json

from dotenv import load_dotenv
load_dotenv()

bot = discord.Bot()

def load_json():

    # Open the JSON file and read its contents
    with open('data.json', 'r') as file:
        data = json.load(file)

    # print(data)
    return data

card_dict = load_json()

def get_color_emoji(c):
    if(c == "白"):
        return "<:type_white:1322043774486057073>"
    if(c == "緑"):
        return "<:type_green:1322044342717911041>"
    if(c == "青"):
        return "<:type_blue:1322044327689584690>"
    if(c == "赤"):
        return "<:type_red:1322044412523581580>"
    if(c == "紫"):
        return "<:type_purple:1322044357787783178>"
    # going to need to add yellow later
    return "<:type_null:1322044371993890937>" # default to colorless/null

def get_color_emoji_cheer(c):
    if(c == "白"):
        return "<:arts_white:1322055132787245109>"
    if(c == "緑"):
        return "<:arts_green:1322055167700504598>"
    if(c == "青"):
        return "<:arts_blue:1322055181789036588>"
    if(c == "赤"):
        return "<:arts_red:1322055071625642054>"
    if(c == "紫"):
        return "<:arts_purple:1322055150361383086>"
    # going to need to add yellow later
    return "<:arts_null:1322055114780966983>" # default to colorless/null

def get_color_emoji_tokkou(c):
    # if weakness damage isn't always +50 this will need to be reworked
    if(c == "白+50"):
        return "<:tokkou_50_white:1322065599186341969>"
    if(c == "緑+50"):
        return "<:tokkou_50_green:1322065548196057190>"
    if(c == "青+50"):
        return "<:tokkou_50_blue:1322065536242290811>"
    if(c == "赤+50"):
        return "<:tokkou_50_red:1322065620837335172>"
    if(c == "紫+50"):
        return "<:tokkou_50_purple:1322065574834077752>"
    # going to need to add yellow later
    return "<:tokkou_50_null:1322065560187572366>" # default to colorless/null
def get_embed_for_card(card, full_size):
    title = card["name"]
    if ("color" in card):
        title = f'{get_color_emoji(card["color"])}{title}'
    # do generic fields
    embed = discord.Embed(title=title, thumbnail=card["image_url"], )
    if(full_size):
        embed = discord.Embed(title=title, image=card["image_url"], description=card["type"])

    
    if ("ホロメン" in card["type"]):
        if("推し" in card["type"]):
            return get_oshi_holomem_embed(card, embed)
        quick_info_string = f'(need emoji){card["bloom_level"]} / HP {card["hp"]} / {card["name"]}'
        embed.add_field(name=quick_info_string, value="", inline=False)

        # arts section
        arts = card["arts"]

        for art in arts:
            cost_str = art["cost"]
            cost_str_pretty = ''
            for c in cost_str:
                cost_str_pretty += get_color_emoji_cheer(c)
            art_desc = ""
            art_desc += "   " + art["damage"]
            if("tokkou" in art):
                art_desc += "   " + get_color_emoji_tokkou(art["tokkou"])+" )  "
            if(art["text"] == ""):
                art_desc += art["name"]
            else:
                art_desc += art["name"] + ": " + art["text"]

            embed.add_field(name=f'( {cost_str_pretty} {art_desc}', value='', inline=False)

        return get_holomem_embed(card, embed)
    embed.add_field(name=card["ability_text"], value='', inline=False)
    return get_support_embed(card, embed) # maybe add cheer/yell/eeru later? could also rename to "get other card embed"

# was going to extract all the specific happenings for each card into these functions later but might not end up doing that
def get_oshi_holomem_embed(card, embed):
    return embed

def get_holomem_embed(card, embed):
    return embed

def get_support_embed(card, embed):
    return embed

def get_generic_embed():
    out = discord.Embed(title = "**title**", color = 0xffffff)
    out.set_author(name="author")
    out.set_thumbnail(url="https://hololive-official-cardgame.com/wp-content/images/cardlist/hSD03/hSD03-013_C.png") # test okanyan
    out.add_field(name="Field 1", value="Field 1 Value", inline=False)
    out.add_field(name="Field 2 (Inline)", value="Field 2 Value", inline=True)
    return out

def get_full_image_embed():
    out = discord.Embed(image="https://hololive-official-cardgame.com/wp-content/images/cardlist/hSD03/hSD03-013_C.png",
                        title="title",
                        description="description")
    return out

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
    print(results)
    return results

find_top_cards(["white","","typeholomem","arts"])

# TODO: work on search feature

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

bot.run(os.getenv('TOKEN'))

