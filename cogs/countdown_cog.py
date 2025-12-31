import discord
from discord.ext import commands, tasks
import datetime
import pytz

class CountdownCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_time_local = 23 # 11 PM
        self.timezone = pytz.timezone('Etc/GMT-6')
        self.countdown_task.start()

    def cog_unload(self):
        self.countdown_task.cancel()

    @tasks.loop(minutes=1.0)
    async def countdown_task(self):
        now = datetime.datetime.now(self.timezone)
        
        # Target is 11 PM today
        target = now.replace(hour=self.target_time_local, minute=0, second=0, microsecond=0)
        
        # If it's already past 11 PM, target is 11 PM tomorrow
        if now >= target:
            target += datetime.timedelta(days=1)
            
        diff = target - now
        total_seconds = int(diff.total_seconds())
        minutes_left = (total_seconds // 60) + 1 # Round up to nearest minute
        
        # Only post if within 60 minutes and exactly on the minute
        # Or you might want it every minute? User said "make a countdown of saying x minute left"
        # I will make it post every minute when it's less than 60 minutes left.
        
        if 0 < minutes_left <= 60:
            CHANNEL_ID = 1336364995721564160
            channel = self.bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(f"{minutes_left} minute{'s' if minutes_left > 1 else ''} left until slime arrives")

    @countdown_task.before_loop
    async def before_countdown(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(CountdownCog(bot))
