import discord
from discord.ext import commands
from discord import app_commands
import json
import io
from helper import send_request


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="help", description="Shows all commands or details about a specific command")
    @app_commands.describe(command="The specific command to get details about")
    @app_commands.choices(command=[
        app_commands.Choice(name="Search", value="search"),
        app_commands.Choice(name="Stats", value="stats"),
        app_commands.Choice(name="Combo", value="combo"),
    ])
    async def help_command(self, interaction: discord.Interaction, command: str = None):
        embed = discord.Embed(title="Help Menu", color=0x6e4790)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)

        if command:
            if command == "search":
                embed.add_field(name="`/search`", value="Searches for given information based on type, input, and year.", inline=False)
                embed.add_field(name="`Usage`", value="```/search <args> <input>```", inline=False)
            elif command == "stats":
                embed.add_field(name="`/stats`", value="Gives statistics about the databases.", inline=False)
                embed.add_field(name="`Usage`", value="```/stats```", inline=False)
            elif command == "combo":
                embed.add_field(name="`/combo`", value="Searches using a combination of data types.", inline=False)
                embed.add_field(name="`Usage`", value="```/combo <args> <input>```", inline=False)
            else:
                embed.add_field(name="Error", value="Command not found.", inline=False)
        else:
            embed.add_field(name="`/search`", value="Searches for given information based on type, input, and year.", inline=False)
            embed.add_field(name="`/stats`", value="Gives statistics about the databases.", inline=False)
            embed.add_field(name="`/combo`", value="Searches using a combination of data types.", inline=False)
            embed.set_footer(text="Use /help <command> for more details on a specific command.")

        await interaction.response.send_message(embed=embed)



























async def setup(bot):
    await bot.add_cog(HelpCog(bot))