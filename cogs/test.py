import discord
from discord.ext import commands
from discord import app_commands

bot_role = "1371775578213978132"
bot_role = discord.utils.get(guild.roles, id=int(bot_role))


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

  @app_commands.command(name="yokoso", description="Yokoso stranger")
  async def yokoso(self, interaction: discord.Interaction):
    await interaction.response.send_message(f"yokoso, {interaction.user.mention}")

  @app_commands.command(name="yahallo", description="Yahallo cool guy")
  async def yahallo_command(self, interaction: discord.Interaction):
    await interaction.response.send_message(f"yahallo {interaction.user.mention}")

  
  @app_commands.command(name="ohayo", description="Greets user with Ohayo")
  async def ohayo(self, interaction: discord.Interaction):
    embedded_msg = discord.Embed(title="Ohayo", description="Ohayo Espada", color=discord.Color.green())
    embedded_msg.set_thumbnail(url='https://i.pinimg.com/originals/a0/9e/ac/a09eacbb0012139bfdb0b75d6eb951b2.gif')
    await interaction.response.send_message(embed=embedded_msg)

  # .......................
  # create channel commands
  # .......................
  
  @app_commands.command(name="create_channel", description="Creates a new text channel")
  async def create_channel(self, interaction: discord.Interaction, channel_name: str):
    guild = interaction.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    category = discord.utils.get(guild.categories, name="RPG Grounds")

    if existing_channel:
      await interaction.response.send_message(f'Ah, so the secretto door to **{channel_name}** is already open, huh? Heaa, no need to knock again ne! But remember, no shenanigansu, desu yo!')
    
    else:
      print(f'Creating a new channel: {channel_name}')
      
      new_channel = await guild.create_text_channel(channel_name, category=category)
      await new_channel.set_permissions(interaction.user, view_channel=True, send_messages=True, create_public_threads=False, create_private_threads=False)
      await new_channel.set_permissions(guild.default_role, view_channel=True, send_messages=False, create_public_threads=False, create_private_threads=False)
      await new_channel.set_permissions(bot_role, view_channel=False, send_messages=False, create_public_threads=False, create_private_threads=False)

      
      
      # Store the channel creator's ID
      await new_channel.edit(topic=f"secretto shopu corner invaided by <@{interaction.user.id}>. Only this customer can manage this part of my shopu.")
      
      await interaction.response.send_message(f'You seemu to have invaided my **{channel_name}** secretto shopu corner, ne? Heaa, take a seeeto—but watch out for the trapsu, desu yo')

  @app_commands.command(name="slime", description="Allow a user to send messages in this channel.")
  async def allow_send_messages(self, interaction: discord.Interaction, target: discord.Member, channel: discord.TextChannel = None):
    channel = channel or interaction.channel  # Default to current channel
    
    if channel.topic == f"secretto shopu corner invaided by <@{interaction.user.id}>. Only this customer can manage this part of my shopu.":
      await channel.set_permissions(target, send_messages=True)
      await interaction.response.send_message(f"Send messages for {target.mention} are now allowed in {channel.mention}.")
    else:  
      await interaction.response.send_message("Only the channel creator can manage permissions.")

  @app_commands.command(name="anti_slime", description="Disallow a user to send messages in this channel.")
  async def disallow_send_messages(self, interaction: discord.Interaction, target: discord.Member, channel: discord.TextChannel = None):
    channel = channel or interaction.channel  # Default to current channel
    
    if channel.topic == f"secretto shopu corner invaided by <@{interaction.user.id}>. Only this customer can manage this part of my shopu." and target != interaction.user.id:
      await channel.set_permissions(target, send_messages=False)
      await interaction.response.send_message(f"Send messages for {target.mention} are now disallowed in {channel.mention}.")    
    else:
      await interaction.response.send_message("Only the channel creator can manage permissions.")

async def setup(bot):
  await bot.add_cog(Test(bot))