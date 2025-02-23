import discord
import emoji_utils

# was going to extract all the specific happenings for each card into these functions later but might not end up doing that
def get_oshi_holomem_embed(card, embed):
    return embed

def get_holomem_embed(card, embed):
    return embed

def get_support_embed(card, embed):
    return embed

def add_divider(embed):
    embed.add_field(name="```────────────────────────────────────────────────────────```", value="", inline=False)
    return

def get_embed_for_card(card, full_size):
    title = card["translated_content_en"]["name"]
    if ("color" in card):
        title = f'{get_color_emoji(card["color"])}{title}'
    # do generic fields
    embed = discord.Embed(title=title, thumbnail=card["image_url"], )
    if(full_size):
        embed = discord.Embed(title=title, image=card["image_url"], description=card["type"])
    embed.set_footer(text=card["id"])

    if ("ホロメン" in card["type"]):
        if("推し" in card["type"]):
            # divider
            add_divider(embed)
            # barebones TL text, need to make the arts cost pretty for holomem
            embed.add_field(name="EN-TL:", value=card["translated_content_en"]["text"], inline=False)
            return get_oshi_holomem_embed(card, embed)
        embed.add_field(name=get_quick_info_string(card), value="", inline=False)
        # effects section
        if ("bloom_effect" in card):
            bloom = card["bloom_effect"]
            bloom_title = f'{emoji_utils.get_bloom_effect_emoji()}: {bloom["name"]}'
            bloom_text = bloom["text"]
            embed.add_field(name=bloom_title,value=bloom_text, inline=False)
        if ("collab_effect" in card):
            collab = card["collab_effect"]
            collab_title = f'{emoji_utils.get_collab_effect()}: {collab["name"]}'
            collab_text = collab["text"]
            embed.add_field(name=collab_title,value=collab_text, inline=False)
        if ("gift_effect" in card):
            gift = card["gift_effect"]
            gift_title = f'{emoji_utils.get_gift_effect_emoji()}: {gift["name"]}'
            gift_text = gift["text"]
            embed.add_field(name=gift_title,value=gift_text, inline=False)

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
            else:
                art_desc += " )  "
            if(art["text"] == ""):
                art_desc += art["name"]
            else:
                art_desc += art["name"] + ": " + art["text"]

            embed.add_field(name=f'( {cost_str_pretty} {art_desc}', value='', inline=False)
        add_divider(embed)
        # barebones TL text, need to make the arts cost pretty for holomem
        embed.add_field(name="EN-TL:", value=card["translated_content_en"]["text"], inline=False)
        return get_holomem_embed(card, embed)
    embed.add_field(name=card["ability_text"], value='', inline=False)
    add_divider(embed)
    # barebones TL text
    embed.add_field(name="EN-TL:", value=card["translated_content_en"]["text"], inline=False)
    return get_support_embed(card, embed) # maybe add cheer/yell/eeru later? could also rename to "get other card embed"