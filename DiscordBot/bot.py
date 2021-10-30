import discord
import asyncio
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

client = Commands.Bot(command_prefix="?", activity = discord.Game(name="💸 Watching the money!"))

@client.event
async def on_ready():
    print('OneWalletWatcher is online!')

@client.command()
async def stats():






client.run(BOT_TOKEN)
