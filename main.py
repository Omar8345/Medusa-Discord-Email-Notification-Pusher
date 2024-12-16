import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import importlib

load_dotenv()

bot_token = os.getenv("TOKEN")
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


@bot.event
async def on_ready():
    print(f"Bot is ready - Logged in as {bot.user}")
    try:
        await load_cogs()
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            cog_name = filename[:-3]
            try:
                importlib.import_module(f"cogs.{cog_name}")
                await bot.load_extension(f"cogs.{cog_name}")
                print(f"Loaded cog: {cog_name}")
            except Exception as e:
                print(f"Failed to load cog {cog_name}: {e}")


bot.run(bot_token)
