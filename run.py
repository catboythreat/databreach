import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=',', intents=intents)

bot.owner_id = 332960819484819456

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    await load_cogs()
    activity = discord.Streaming(name="catboy is cool", url="http://twitch.tv/streamer")
    await bot.change_presence(activity=activity)
    await bot.tree.sync()


bot.run(os.getenv('TOKEN'))
