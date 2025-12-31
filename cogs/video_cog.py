import discord
from discord.ext import commands
import os

class VideoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sendvideo")
    async def send_video(self, ctx):
        """Sends an embed with a video from the assets folder"""
        video_path = "assets/videos/your_video.mp4"
        
        if not os.path.exists(video_path):
            await ctx.send("Video file not found! Please upload 'your_video.mp4' to the 'assets/videos' folder.")
            return

        file = discord.File(video_path, filename="video.mp4")
        embed = discord.Embed(title="Check out this video!", description="Playing uploaded video")
        
        # Note: Discord doesn't support direct video playback inside an embed "video" field via local files.
        # We attach it as a file which Discord then displays as a playable video below the embed.
        await ctx.send(file=file, embed=embed)

async def setup(bot):
    await bot.add_cog(VideoCog(bot))
