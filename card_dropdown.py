import discord
from emoji_utils import get_quick_info_string
from embeds import get_embed_for_card
class CardDropdown(discord.ui.Select):
    def __init__(self, cards):
        options = [
            discord.SelectOption(label=f"{idx+1}", value=card["id"])
            for idx, card in enumerate(cards)
        ]
        self.cards = cards
        super().__init__(placeholder="Select a card...", min_values=1, max_values=1,
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_card_id = self.values[0]
        for card in self.cards:
            if card["id"] == selected_card_id:
                embed = get_embed_for_card(card, True)
                await interaction.response.send_message(embed=embed)
                return
        await interaction.response.send_message("No matching card found.")