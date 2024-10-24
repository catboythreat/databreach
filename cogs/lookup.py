import discord
from discord.ext import commands
from discord import app_commands
import json
import io
from helper import send_request

class LookupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_guild_channel(self, interaction: discord.Interaction):
        if interaction.channel is None or isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message("This command cannot be used in DMs.", ephemeral=True)
            return False
        return True

    @app_commands.command(name="search", description="Searches for given information based on type, input, and year.")
    async def lookup_info(
        self,
        interaction: discord.Interaction,
        type: str,
        input: str,
        year: int = 2000,
        ephemeral: bool = False
    ):
        if not await self.is_guild_channel(interaction):
            return
        
        if not input:
            await interaction.response.send_message("Please provide a value to search.", ephemeral=ephemeral)
            return
        
        search_response = send_request('data/search', {
            'terms': [input],
            'types': [type],
            'wildcard': False,
        })

        if search_response.get("size", 0) == 0:
            await interaction.response.send_message(f"No results found for the {type}: {input}.", ephemeral=True)
            return

        filtered_results = {}
        for dataset, entries in search_response.get("results", {}).items():
            try:
                dataset_year = int(dataset[-4:])
            except ValueError:
                continue
            
            if dataset_year < year:
                continue

            matched_entries = []
            for entry in entries:
                if (type == "username" and entry.get("username") == input) or \
                    (type == "email" and entry.get("email") == input) or \
                    (type == "name" and entry.get("name") == input) or \
                    (type == "_domain" and entry.get("_domain") == input) or \
                    (type == "password" and entry.get("password") == input):
                    matched_entries.append(entry)

            if matched_entries:
                filtered_results[dataset] = matched_entries

        if not filtered_results:
            await interaction.response.send_message(f"No results found for the {type}: {input} from {year} onward.", ephemeral=True)
            return

        text_result = json.dumps({"results": filtered_results}, indent=4)
        text_file = io.BytesIO(text_result.encode('utf-8'))
        text_file.name = f"{input}_result.txt"

        await interaction.response.send_message(file=discord.File(text_file, text_file.name), ephemeral=ephemeral)

    @lookup_info.autocomplete("type")
    async def lookup_type_autocomplete(self, interaction: discord.Interaction, current: str):
        choices = [
            app_commands.Choice(name="Email", value="email"),
            app_commands.Choice(name="Username", value="username"),
            app_commands.Choice(name="Full Name", value="name"),
            app_commands.Choice(name="Domain", value="_domain"),
            app_commands.Choice(name="Password", value="password"),
        ]
        return [choice for choice in choices if current.lower() in choice.name.lower()]

    @app_commands.describe(year="Select the year from which to show results")
    @app_commands.choices(year=[
        app_commands.Choice(name="2019", value=2019),
        app_commands.Choice(name="2020", value=2020),
        app_commands.Choice(name="2021", value=2021),
        app_commands.Choice(name="2022", value=2022),
        app_commands.Choice(name="2023", value=2023),
    ])
    async def lookup_year_autocomplete(self, interaction: discord.Interaction, current: int):
        return [app_commands.Choice(name=str(year), value=year) for year in range(2019, 2024) if str(year).startswith(str(current))]

    @app_commands.command(name="combo", description="Searches using a combination of data types.")
    async def combo_search(
        self,
        interaction: discord.Interaction,
        choice1: str,
        input1: str,
        choice2: str,
        input2: str,
        ephemeral: bool = False
    ):
        if not await self.is_guild_channel(interaction):
            return

        if not input1 or not input2:
            await interaction.response.send_message("Please provide values for both inputs.", ephemeral=ephemeral)
            return

        search_responses = []
        for choice, input_value in [(choice1, input1), (choice2, input2)]:
            response = send_request('data/search', {
                'terms': [input_value],
                'types': [choice],
                'wildcard': False,
            })
            if response.get("size", 0) > 0:
                search_responses.append(response.get("results", {}))
            else:
                await interaction.response.send_message(f"No results found for the {choice}: {input_value}.", ephemeral=ephemeral)
                return

        combined_results = {}

        results_choice1 = search_responses[0]
        results_choice2 = search_responses[1]

        for dataset in results_choice1:
            if dataset in results_choice2:
                for entry in results_choice1[dataset]:
                    if entry.get('username') == input1:
                        for entry2 in results_choice2[dataset]:
                            if entry2.get('email') == input2:
                                if dataset not in combined_results:
                                    combined_results[dataset] = []
                                combined_results[dataset].append(entry)

        if not combined_results:
            await interaction.response.send_message("No exact matches found for both inputs.", ephemeral=ephemeral)
            return

        all_matched_results = {
            "matched_results": combined_results
        }

        text_result = json.dumps(all_matched_results, indent=4)
        text_file = io.BytesIO(text_result.encode('utf-8'))
        text_file.name = f"{input1}_{input2}_matched_results.txt"

        await interaction.response.send_message(file=discord.File(text_file, text_file.name), ephemeral=ephemeral)

    @combo_search.autocomplete("choice1")
    @combo_search.autocomplete("choice2")
    async def combo_choice_autocomplete(self, interaction: discord.Interaction, current: str):
        choices = [
            app_commands.Choice(name="Email", value="email"),
            app_commands.Choice(name="Username", value="username"),
            app_commands.Choice(name="Full Name", value="name"),
            app_commands.Choice(name="_domain", value="_domain"),
            app_commands.Choice(name="Password", value="password"),
        ]
        return [choice for choice in choices if current.lower() in choice.name.lower()]

async def setup(bot):
    await bot.add_cog(LookupCog(bot))
