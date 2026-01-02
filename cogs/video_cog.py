import discord
from discord.ext import commands
import os
import aiocron
import pytz
from datetime import datetime

class VideoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Schedule for daily video at 8:00 PM GMT+6
        try:
            self.daily_video_task = aiocron.crontab('30 18 * * *', func=self.send_scheduled_video, tz=pytz.timezone('Etc/GMT-6'))
        except Exception as e:
            print(f"Cron setup error: {e}")

   
    async def send_scheduled_video(self):
        """Internal function to send the video to a specific channel"""
        # Replace with your actual channel ID where you want the video sent
        CHANNEL_ID =  1336364995721564160  #1455926797882490992 YOU MUST UPDATE THIS
        channel = self.bot.get_channel(CHANNEL_ID)
        
        if channel:
            video_path = "assets/videos/Oreki sad edit  amvedit.mp4"
            if os.path.exists(video_path):
                # Discord's file size limit is 25MB for free users, but sometimes 
                # uploads fail slightly below that or due to network issues.
                # We'll use a conservative 24MB limit to be safe.
                
                file = discord.File(video_path, filename="video.mp4")
                embed = discord.Embed(
                    title="I feel like I have lost something...",
                    description="-# Why does it feels so lonely....and empty?",
                        color=discord.Color.dark_grey()
                    )
                await channel.send(content="@everyone", file=file, embed=embed)
            else:
                print(f"Scheduled task failed: {video_path} not found")
        else:
            print(f"Scheduled task failed: Channel {CHANNEL_ID} not found")

    @commands.command(name="sendvideo")
    async def send_video(self, ctx):
        """Sends an embed with a video from the assets folder"""
        video_path = "assets/videos/SLAVA FUNK! (SLOWED) - AIZEN.mp4"
        
        if not os.path.exists(video_path):
            await ctx.send(f"Video file not found at {video_path}!")
            return

        file_size = os.path.getsize(video_path)
        if file_size > 24 * 1024 * 1024:
            await ctx.send(f"⚠️ Video is too large ({file_size/1024/1024:.2f}MB). Max limit is 25MB.")
            return

        file = discord.File(video_path, filename="video.mp4")
        embed = discord.Embed(
            title="Something stirs within you, compelling your heart to race relentlessly.", 
            description="-# One such as I, whose presence has been long awaited, has finally returned.",
            color=discord.Color.dark_grey()
        )
        await ctx.send(content="@everyone", file=file, embed=embed)

    @discord.app_commands.command(name="send_video", description="Send the special video in this channel")
    async def slash_send_video(self, interaction: discord.Interaction):
        """Slash command to send the video"""
        video_path = "assets/videos/SLAVA FUNK! (SLOWED) - AIZEN.mp4"
        
        if not os.path.exists(video_path):
            await interaction.response.send_message(f"Video file not found at {video_path}!", ephemeral=True)
            return

        file_size = os.path.getsize(video_path)
        if file_size > 24 * 1024 * 1024:
            await interaction.response.send_message(f"⚠️ Video is too large ({file_size/1024/1024:.2f}MB). Max limit is 25MB.", ephemeral=True)
            return

        # Defer because uploading might take a moment
        await interaction.response.defer()
        
        file = discord.File(video_path, filename="video.mp4")
        embed = discord.Embed(
            title="Something stirs within you, compelling your heart to race relentlessly.", 
            description="-# One such as I, whose presence has been long awaited, has finally returned.",
            color=discord.Color.dark_grey()
        )
        await interaction.followup.send(content="@everyone", file=file, embed=embed)

async def setup(bot):
    await bot.add_cog(VideoCog(bot))
