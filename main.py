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
  "Want some candy? I promise it’s not laced with anything... this time",
  
  "Ah, advice? I charge a fee for that. How about a nice hat instead?", "Prepare yourself! I’m about to unveil my master plan... or maybe just a really good snack recipe.",
  
  "Welcome to my shop! We have everything from soul candy to soul-saving advice. Just don’t ask about the ‘mystery’ section!",
  
  "Introducing the latest in soul-reaping technology! Guaranteed to be 50% more stylish than the last model!"])

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