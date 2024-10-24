import discord
from discord.ext import commands
from discord import app_commands
import json
import io
from helper import send_request

class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stats", description="Retrieve database statistics.")
    async def stats_info(self, interaction: discord.Interaction):
        stats_response = send_request('data/stats')

        if not stats_response:
            await interaction.response.send_message("Failed to retrieve statistics.", ephemeral=True)
            return

        stats_message = json.dumps(stats_response, indent=4)
        text_file = io.BytesIO(stats_message.encode('utf-8'))
        text_file.name = "stats_result.txt"

        await interaction.response.send_message(file=discord.File(text_file, text_file.name))


    @app_commands.command(name="buy", description="Fetch different purchase options.")
    async def purchase(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Puchase Sentinel",
            description="Purchase with cryptocurrency [here](https://sentinelbot.mysellix.io/) \n Purchase with PayPal here: https://discord.com/channels/1288908059124568096/1290667800410722344",
            color=0x6e4790
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)












async def setup(bot):
    await bot.add_cog(MiscCog(bot))