import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import asyncio
from itertools import cycle
import web

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


bot_statuses = cycle([
    "Defending against an army of slime",
    "King Slime is too strong!",
    "Keeps all slimes away except king slime"
])

@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(bot_statuses)))

@bot.event
async def on_ready():
  change_status.start()
  




async def load():
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    async with bot:
        await load()
        await bot.start(os.getenv('TOKEN'))

web.keep_alive()
asyncio.run(main())