import discord
from discord.ext import commands
from discord import app_commands



class Test(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print(f"{self.__class__.__name__} is ready")
    print("Yokoso watashi no slime society")
    try:
      synced = await self.bot.tree.sync()
      print(f"Synced {len(synced)} command(s)")
    except Exception as e:
      print("Error syncing commands:", e)
    
  @app_commands.command(name="ping", description="returns the latency")
  async def ping(self, interaction: discord.Interaction):
    ping_embed = discord.Embed(title="Ping!", description=f"Ping: {round(self.bot.latency * 1000)}ms", color=discord.Color.green())
    await interaction.response.send_message(embed=ping_embed)
  
  @app_commands.command(name="help", description="Shows available commands")
  async def help(self, interaction: discord.Interaction):
    help_embed = discord.Embed(title="Command List", description="Displays a list of available commands.", color=discord.Color(0xff9776))
    help_embed.add_field(name="/ping", value="Returns the bot's latency.", inline=False)
    help_embed.add_field(name="/create_channel", value="Creates a new text channel.", inline=False)
    help_embed.add_field(name="/slime", value="Allow a user to send messages in this channel.", inline=False)
    help_embed.add_field(name="/anti_slime", value="Disallow a user to send messages in this channel.", inline=False)
    await interaction.response.send_message(embed=help_embed)
  
  # .......................
  # create channel commands
  # .......................
  
  @app_commands.command(name="create_channel", description="Creates a new text channel")
  async def create_channel(self, interaction: discord.Interaction, channel_name: str):
    guild = interaction.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    category = discord.utils.get(guild.categories, name="ＴＲ－ＧＲＯＵＮＤＳ")

    # Check if the user already owns a channel
    owned_channel = discord.utils.find(lambda c: c.topic and f"<@{interaction.user.id}>" in c.topic, guild.text_channels)

    if owned_channel:
      await interaction.response.send_message(f'Looks like you already claimed {owned_channel.mention} as your personal dumpster! Only one dumpster per person allowed!')
      return


    if existing_channel:
      await interaction.response.send_message(f'Looks like the dumpster **{channel_name}** is already overflowing! No more trash allowed for now, ya hear?!')
    
    else:
      print(f'Creating a new channel: {channel_name}')
      
      new_channel = await guild.create_text_channel(channel_name, category=category)
      await new_channel.set_permissions(interaction.user, view_channel=True, send_messages=True, create_public_threads=False, create_private_threads=False)
      await new_channel.set_permissions(guild.default_role, view_channel=True, send_messages=False, create_public_threads=False, create_private_threads=False)
      
      
      # Store the channel creator's ID
      await new_channel.edit(topic=f"Designated trash zone claimed by <@{interaction.user.id}>.  This garbage belongs to them.")
      
      await interaction.response.send_message(f'You claimed **{channel_name}** as your personal dumpster! Enjoy the stench!')

  @app_commands.command(name="slime", description="Allow a user to send messages in this channel.")
  async def allow_send_messages(self, interaction: discord.Interaction, target: discord.Member, channel: discord.TextChannel = None):
    channel = channel or interaction.channel  # Default to current channel
    
    if channel.topic == f"Designated trash zone claimed by <@{interaction.user.id}>.  This garbage belongs to them.":
      await channel.set_permissions(target, send_messages=True, view_channel=True)
      await interaction.response.send_message(f"Now accepting trash from {target.mention} in {channel.mention}.")
    else:  
      await interaction.response.send_message("Only the garbage owner can manage permissions.")

  
  @app_commands.command(name="anti_slime", description="Disallow a user to send messages in this channel.")
  async def disallow_send_messages(self, interaction: discord.Interaction, target: discord.Member, channel: discord.TextChannel = None):
    channel = channel or interaction.channel  # Default to current channel

    if target != interaction.user:
      if channel.topic == f"Designated trash zone claimed by <@{interaction.user.id}>.  This garbage belongs to them.":
        await channel.set_permissions(target, send_messages=False)
        await interaction.response.send_message(f"No more trash from {target.mention} allowed in {channel.mention}.")    
      else:
        await interaction.response.send_message("Only the garbage owner can manage permissions.")
    else:
      await interaction.response.send_message("You can't ban yourself from your own trash.")

  
  @app_commands.command(name="rename_dumpster", description="Rename the channel if you own it.")
  async def rename_channel(self, interaction: discord.Interaction, channel: discord.TextChannel, new_name: str): 
    channel = channel or interaction.channel
    if channel and channel.topic and f"<@{interaction.user.id}>" in channel.topic:
      try:
        await channel.edit(name=new_name)
        await interaction.response.send_message(f"Successfully renamed your dumpster to **{new_name}**!", ephemeral=True)
      except discord.errors.Forbidden:
        await interaction.response.send_message("I don't have permission to rename this channel.", ephemeral=True)
      except discord.errors.HTTPException as e:
        await interaction.response.send_message(f"Failed to rename channel: {e}", ephemeral=True)
    else:
      await interaction.response.send_message("You do not own this dumpster, you can't rename it.", ephemeral=True)

  @app_commands.command(name="claim_dumpster", description="Claim ownership of an existing channel.")
  async def claim_channel(self, interaction: discord.Interaction, target: discord.Member, channel: discord.TextChannel = None):
    channel = channel or interaction.channel

    # Check if the channel already has an owner
    if channel.topic and "Designated trash zone claimed by" in channel.topic:
      await interaction.response.send_message("This dumpster already has an owner!", ephemeral=True)
      return

    guild = interaction.guild
    owned_channel = discord.utils.find(lambda c: c.topic and f"<@{target.id}>" in c.topic, guild.text_channels)

    if owned_channel:
      await interaction.response.send_message(f'Looks like {target.mention} already claimed {owned_channel.mention} as their personal dumpster! Only one dumpster per person allowed!', ephemeral=True)
      return
    
    try:
      await channel.edit(topic=f"Designated trash zone claimed by <@{target.id}>.  This garbage belongs to them.")
      await channel.set_permissions(target, view_channel=True, send_messages=True, create_public_threads=False, create_private_threads=False)
      await interaction.response.send_message(f"You have claimed {channel.mention} for {target.mention} as their personal dumpster!", ephemeral=True)
    except discord.errors.Forbidden:
      await interaction.response.send_message("I don't have the necessary permissions to edit this channel.", ephemeral=True)
    except Exception as e:
      await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
      
async def setup(bot):
  await bot.add_cog(Test(bot))