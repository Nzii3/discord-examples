# REQUIRED IMPORTS
import discord
from discord.ext import commands

# OPTIONAL IMPORTS
from discord.commands import slash_command, permissions, Option

class Kick(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
### PREFIX COMMAND ###
  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided."):
    await ctx.trigger_typing()
    if member == ctx.author:
      return await ctx.reply("You can't kick yourself.") #self explanatory 
    if member.top_role >= ctx.author.top_role: # checks to see if the user is trying to kick a user higher than them (e.g. Staff member trying to kick Management member)
      return await ctx.reply("You can't kick a user that's higher than you.")
    # creating an embed to send to the member
    embed = discord.Embed(color=discord.Colour.red(), description=f"You've been kicked from {ctx.guild.name}!")
    embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon if ctx.guild.icon else "https://media.pocketgamer.biz/2021/5/110514/discord-new-logo-2021-r225x.jpg") # Now, this is a big thing: pycord changed the way the 'OBJECT.icon/avatar_url' works. it might throw an error if 'ctx.guild' doesn't have an icon; I recommend leaving it how it is if you're using pycord, if you're using discord.py, change '.icon' > '.icon_url'
    embed.add_field(name="Reason", value=reason)
    try:
      await member.send(embed=embed)
    except discord.Forbidden:
      pass # ignoring that the member couldn't be messaged
    try:
      await member.kick(reason=reason)
    except discord.Forbidden: # if you're using discord.py, use 'discord.errors.Forbidden' instead of 'discord.Forbiddn'; means the bot can't kick the user
      return await ctx.reply(f"Could not kick {member}; please make sure I have `Kick Members` permissions.")
    await ctx.reply(f"🔨 Kicked`{member}`\n**Reason:** {reason}") # you can pass in 'mention_author=False' if you don't want the bot to ping the author when replying. By default it pings.

### SLASH COMMAND

  @slash_command(guild_ids=[123456789]) # Replace '123...' with the ID you want your bot to add the slash command to
  @permissions.has_permissions(kick_members=True)
  async def kick(self, ctx, member: Option(discord.Member, "Member to kick", required=True), reason: Option(str, "Reason", default="No reason provided.")): # If a reason is a NoneType (none), it defaults to 'No reason provided.'
    await ctx.defer()
    if member == ctx.author:
      return await ctx.interaction.followup.send("You can't kick yourself.") #self explanatory 
    if member.top_role >= ctx.author.top_role: # checks to see if the user is trying to kick a user higher than them (e.g. Staff member trying to kick Management member)
      return await ctx.interaction.followup.send("You can't kick a user that's higher than you.")
    # creating an embed to send to the member
    embed = discord.Embed(color=discord.Colour.red(), description=f"You've been kicked from {ctx.guild.name}!")
    embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon if ctx.guild.icon else "https://media.pocketgamer.biz/2021/5/110514/discord-new-logo-2021-r225x.jpg") # Now, this is a big thing: pycord changed the way the 'OBJECT.icon/avatar_url' works. it might throw an error if 'ctx.guild' doesn't have an icon; I recommend leaving it how it is if you're using pycord, if you're using discord.py, change '.icon' > '.icon_url'
    embed.add_field(name="Reason", value=reason)
    try:
      await member.send(embed=embed)
    except discord.Forbidden:
      pass # ignoring that the member couldn't be messaged
    try:
      await member.kick(reason=reason)
    except discord.Forbidden: # if you're using discord.py, use 'discord.errors.Forbidden' instead of 'discord.Forbiddn'; means the bot can't kick the user
      return await ctx.interaction.followup.send(f"Could not kick {member}; please make sure I have `Kick Members` permissions.")
    await ctx.interaction.followup.send(f"🔨 Kicked `{member}`\n**Reason:** {reason}")

def setup(bot: commands.Bot):
  bot.add_cog(Kick(bot))
