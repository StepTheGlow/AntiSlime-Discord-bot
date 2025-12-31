import discord
from discord.ext import commands
import os
import aiocron
import pytz
from datetime import datetime

class VideoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Schedule for 8 PM (20:00) in GMT+6
        # Cron format: 'minute hour day month day_of_week'
        # '0 20 * * *' means 8:00 PM every day
        self.daily_video_task = aiocron.crontab('0 20 * * *', func=self.send_scheduled_video, tz=pytz.timezone('Etc/GMT-6'))

    async def send_scheduled_video(self):
        """Internal function to send the video to a specific channel"""
        # Replace with your actual channel ID where you want the video sent
        CHANNEL_ID = 123456789012345678  # YOU MUST UPDATE THIS
        channel = self.bot.get_channel(CHANNEL_ID)
        
        if channel:
            video_path = "assets/videos/your_video.mp4"
            if os.path.exists(video_path):
                file = discord.File(video_path, filename="video.mp4")
                embed = discord.Embed(
                    title="Custom Heading Here", 
                    description=f"Scheduled video for {datetime.now(pytz.timezone('Etc/GMT-6')).strftime('%Y-%m-%d %H:%M')}\n\n-# Small bottom text here"
                )
                await channel.send(file=file, embed=embed)
            else:
                print(f"Scheduled task failed: {video_path} not found")
        else:
            print(f"Scheduled task failed: Channel {CHANNEL_ID} not found")

    @commands.command(name="sendvideo")
    async def send_video(self, ctx):
        """Sends an embed with a video from the assets folder"""
        video_path = "assets/videos/your_video.mp4"
        
        if not os.path.exists(video_path):
            await ctx.send("Video file not found! Please upload 'your_video.mp4' to the 'assets/videos' folder.")
            return

        file = discord.File(video_path, filename="video.mp4")
        embed = discord.Embed(
            title="Custom Heading Here", 
            description="Playing uploaded video\n\n-# Small bottom text here"
        )
        
        # Note: Discord doesn't support direct video playback inside an embed "video" field via local files.
        # We attach it as a file which Discord then displays as a playable video below the embed.
        await ctx.send(file=file, embed=embed)

async def setup(bot):
    await bot.add_cog(VideoCog(bot))
