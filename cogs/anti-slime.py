import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio


class Test(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
      self.command_locks = {}  # Dictionary to store locks for each command

  @commands.Cog.listener()
  async def on_ready(self):
    print(f"{self.__class__.__name__} is ready")
    print("Yokoso watashi no slime society")
    try:
      synced = await self.bot.tree.sync()
      print(f"Synced {len(synced)} command(s)")
    except Exception as e:
      print("Error syncing commands:", e)
    
  async def acquire_lock(self, interaction: discord.Interaction, command_name: str):
    """Acquires a lock for a specific command, preventing rate limits."""
    user_id = interaction.user.id
    command_key = f"{command_name}:{user_id}"

    if command_key in self.command_locks and self.command_locks[command_key].locked():
      await interaction.response.send_message("Please wait, this command is still processing.", ephemeral=True)
      return False

    self.command_locks[command_key] = asyncio.Lock()
    await self.command_locks[command_key].acquire()
    return True

  def release_lock(self, interaction: discord.Interaction, command_name: str):
    """Releases the lock for a specific command."""
    user_id = interaction.user.id
    command_key = f"{command_name}:{user_id}"

    if command_key in self.command_locks and self.command_locks[command_key].locked():
      self.command_locks[command_key].release()

  @app_commands.command(name="ping", description="returns the latency")
  async def ping(self, interaction: discord.Interaction):
    if not await self.acquire_lock(interaction, "ping"):
      return
    try:
      ping_embed = discord.Embed(title="Ping!", description=f"Ping: {round(self.bot.latency * 1000)}ms", color=discord.Color.green())
      await interaction.response.send_message(embed=ping_embed)
    finally:
      self.release_lock(interaction, "ping")
  
  @app_commands.command(name="help", description="Shows available commands")
  async def help(self, interaction: discord.Interaction):
    if not await self.acquire_lock(interaction, "help"):
      return
    try:
      help_embed = discord.Embed(title="Command List", description="Displays a list of available commands.", color=discord.Color(0xff9776))
      help_embed.add_field(name="/ping", value="Returns the bot's latency.", inline=False)
      help_embed.add_field(name="/create_channel", value="Creates a new text channel.", inline=False)
      help_embed.add_field(name="/slime", value="Allow a user to send messages in this channel.", inline=False)
      help_embed.add_field(name="/anti_slime", value="Disallow a user to send messages in this channel.", inline=False)
      help_embed.add_field(name="/rename_dumpster", value="Rename the channel if you own it.", inline=False)
      await interaction.response.send_message(embed=help_embed)
    finally:
      self.release_lock(interaction, "help")
  
  # .......................
  # create channel commands
  # .......................
  
  @app_commands.command(name="create_channel", description="Creates a new text channel")
  async def create_channel(self, interaction: discord.Interaction, emoji: str, channel_name: str):
    if not await self.acquire_lock(interaction, "create_channel"):
      return
    try:
      guild = interaction.guild
      final_channel_name = f"{emoji}{channel_name}"
      existing_channel = discord.utils.get(guild.channels, name=final_channel_name)
      category = discord.utils.get(guild.categories, name="ＴＲ－ＧＲＯＵＮＤＳ")

      # Check if the user already owns a channel
      owned_channel = discord.utils.find(lambda c: c.topic and f"<@{interaction.user.id}>" in c.topic, guild.text_channels)

      if owned_channel:
        await interaction.response.send_message(f'Looks like you already claimed {owned_channel.mention} as your personal dumpster! Only one dumpster per person allowed!')
        return


      if existing_channel:
        await interaction.response.send_message(f'Looks like the dumpster **{final_channel_name}** is already overflowing! No more trash allowed for now, ya hear?!')
      
      else:
        print(f'Creating a new channel: {final_channel_name}')
        
        new_channel = await guild.create_text_channel(final_channel_name, category=category)
        await new_channel.set_permissions(interaction.user, view_channel=True, send_messages=True, create_public_threads=False, create_private_threads=False, manage_messages=True)
        await new_channel.set_permissions(guild.default_role, view_channel=True, send_messages=False, create_public_threads=False, create_private_threads=False)
        
        
        # Store the channel creator's ID
        await new_channel.edit(topic=f"Designated trash zone claimed by <@{interaction.user.id}>.  This garbage belongs to them.")
        
        await interaction.response.send_message(f'You claimed **{final_channel_name}** as your personal dumpster! Enjoy the stench!')
    finally:
      self.release_lock(interaction, "create_channel")

  @app_commands.command(name="slime", description="Allow a user to send messages in this channel.")
  async def allow_send_messages(self, interaction: discord.Interaction, target: discord.Member, channel: discord.TextChannel = None):
    if not await self.acquire_lock(interaction, "slime"):
      return
    try:
      channel = channel or interaction.channel  # Default to current channel
      
      if channel.topic == f"Designated trash zone claimed by <@{interaction.user.id}>.  This garbage belongs to them.":
        await channel.set_permissions(target, send_messages=True, view_channel=True)
        await interaction.response.send_message(f"Now accepting trash from {target.mention} in {channel.mention}.")
      else:  
        await interaction.response.send_message("Only the garbage owner can manage permissions.")
    finally:
      self.release_lock(interaction, "slime")

  
  @app_commands.command(name="anti_slime", description="Disallow a user to send messages in this channel.")
  async def disallow_send_messages(self, interaction: discord.Interaction, target: discord.Member, channel: discord.TextChannel = None):
    if not await self.acquire_lock(interaction, "anti_slime"):
      return
    try:
      channel = channel or interaction.channel  # Default to current channel

      if target != interaction.user:
        if channel.topic == f"Designated trash zone claimed by <@{interaction.user.id}>.  This garbage belongs to them.":
          await channel.set_permissions(target, send_messages=False)
          await interaction.response.send_message(f"No more trash from {target.mention} allowed in {channel.mention}.")    
        else:
          await interaction.response.send_message("Only the garbage owner can manage permissions.")
      else:
        await interaction.response.send_message("You can't ban yourself from your own trash.")
    finally:
      self.release_lock(interaction, "anti_slime")

  
  @app_commands.command(name="rename_dumpster", description="Rename the channel if you own it.")
  async def rename_channel(self, interaction: discord.Interaction, emoji: str, new_name: str, channel: discord.TextChannel = None):
    if not await self.acquire_lock(interaction, "rename_dumpster"):
      return
    try:
      final_channel_name = f"{emoji}{new_name}"
      channel = channel or interaction.channel
      if channel.topic == f"Designated trash zone claimed by <@{interaction.user.id}>.  This garbage belongs to them.":
        await channel.edit(name=final_channel_name)
        await interaction.followup.send(f"Successfully renamed your dumpster to **{final_channel_name}**!")  # Use followup
      else:
        await interaction.followup.send("You do not own this dumpster, you can't rename it.", ephemeral=True)  # Use followup
    finally:
      self.release_lock(interaction, "rename_dumpster")

async def setup(bot):
  await bot.add_cog(Test(bot))