import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import asyncio
from itertools import cycle

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


bot_statuses = cycle([
  "Want some candy? I promise it’s not laced with anything... this time",
  
  "Ah, advice? I charge a fee for that. How about a nice hat instead?", "Prepare yourself! I’m about to unveil my master plan... or maybe just a really good snack recipe.",
  
  "Welcome to my shop! We have everything from slime candy to food-saving advice. Just don’t ask about the ‘mystery’ section!",
  
  "Introducing the latest in-slime technology! Guaranteed to be 50% more stylish than the last model!"]) 
# slime candy is soul candy food-saving is soul saving  in-slime is in soul-reaping

@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(bot_statuses)))

@bot.event
async def on_ready():
  change_status.start()
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
    for cmd in synced:
        print(f"Synced command: {cmd.name}")
  except Exception as e:
    print("Error syncing commands:", e)

@bot.tree.command(name="yahallo", description="yahallo cool guy")
async def yahallo(interaction: discord.Interaction):
  latency = round(bot.latency * 1000)
  await interaction.response.send_message(f"yahallo {interaction.user.mention}")
  await interaction.response.send_message(f"Pong! Latency: {latency}ms")

async def load():
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.endswith('.disabled'):
      try:
        await bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded extension: {filename}")
      except Exception as e:
        print(f"Failed to load extension {filename}: {e}")

async def main():
    token = os.getenv('TOKEN')
    if not token:
        print("❌ TOKEN not found in environment variables!")
        return

    retry_delay = 5
    while True:
        try:
            async with bot:
                await load()
                await bot.start(token)
        except discord.errors.HTTPException as e:
            if e.status == 429:
                print(f"⚠️ Rate limited by Discord. Waiting {retry_delay}s before retrying...")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 300)
            else:
                print(f"❌ HTTP error: {e}")
                await asyncio.sleep(retry_delay)
        except Exception as e:
            print(f"❌ Error starting bot: {e}")
            await asyncio.sleep(retry_delay)
        else:
            break

asyncio.run(main())