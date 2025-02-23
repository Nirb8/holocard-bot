def get_bloom_level_emoji(level):
    if (level.lower() == "debut"):
        return "<:debut:1323350942875385940>"
    if (level.lower() == "1st"):
        return "<:1st:1323350839850438770>"
    if (level.lower() == "2nd"):
        return "<:2nd:1323350857479229592>"
    if (level.lower() == "spot"):
        return "<:spot:1323350993508765726>"
    return ""
def get_buzz_emoji(type):
    if ("buzz" in type.lower()):
        return "<:buzz:1323350892484755566>"
    return ""

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

def get_collab_effect_emoji():
    return "<:collab_effect:1323350914073100338>"

def get_gift_effect_emoji():
    return "<:gift:1323350975972380743>"

def get_bloom_effect_emoji():
    return "<:bloom_effect:1323351068335411220>"


def get_quick_info_string(card, verbose=False):
    info_parts = []
    if "bloom_level" in card:
        info_parts.append(get_bloom_level_emoji(card["bloom_level"]))
    if "type" in card:
        info_parts.append(get_buzz_emoji(card["type"]))
    if "hp" in card:
        info_parts.append(f'HP {card["hp"]}')
    elif "life" in card:
        info_parts.append(f'LIFE {card["life"]}')

    info_parts.append(card["name"])

    if verbose and "rarity" in card:
        info_parts.append(card["rarity"])
    if "bloom_effect" in card:
        info_parts.append(get_bloom_effect_emoji())
    if "collab_effect" in card:
        info_parts.append(get_collab_effect_emoji())
    if "gift_effect" in card:
        info_parts.append(get_gift_effect_emoji())
    return ' / '.join(info_parts)
