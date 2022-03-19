# REQUIRED IMPORTS
import discord
from discord.ext import commands

# OPTIONAL IMPORTS
from discord.commands import slash_command, permissions, Option # for ban slash command

class Ban(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
### PREFIX COMMAND (commands.Bot needed when defining client var) ###
  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided.", delete_message_days: int=None): # 'delete_message_days' is when Discord automatically deletes messages sent by the banned user in the server
    await ctx.trigger_typing()
    if delete_message_days <= 7:
      delete_message_days = 7 # Discord doesn't allow messages older than 7 days to be deleted in this method, so we change it to 7 and move on 
    if member == ctx.author:
      return await ctx.reply("You can't ban yourself.") #self explanatory 
    if member.top_role >= ctx.author.top_role: # checks to see if the user is trying to ban a user higher than them (e.g. Staff member trying to ban Management member)
      return await ctx.reply("You can't ban a user that's higher than you.")
    # creating an embed to send to the member
    embed = discord.Embed(color=discord.Colour.red(), description=f"You've been banned in {ctx.guild.name}!")
    embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon if ctx.guild.icon else "https://media.pocketgamer.biz/2021/5/110514/discord-new-logo-2021-r225x.jpg") # Now, this is a big thing: pycord changed the way the 'OBJECT.icon/avatar_url' works. it might throw an error if 'ctx.guild' doesn't have an icon; I recommend leaving it how it is if you're using pycord, if you're using discord.py, change '.icon' > '.icon_url'
    embed.add_field(name="Reason", value=reason)
    try:
      await member.send(embed=embed)
    except discord.Forbidden:
      pass # ignoring that the member couldn't be messaged
    try:
      await member.ban(reason=reason, delete_message_days=delete_message_days)
    except discord.Forbidden: # if you're using discord.py, use 'discord.errors.Forbidden' instead of 'discord.Forbiddn'; means the bot can't ban the user
      return await ctx.reply(f"Could not ban {member}; please make sure I have `Ban Members` permissions.")
    await ctx.reply(f"🔨 Banned `{member}`\n**Reason:** {reason}") # you can pass in 'mention_author=False' if you don't want the bot to ping the author when replying. By default it pings.

### SLASH COMMAND

  @slash_command(guild_ids=[123456789]) # Replace '123...' with the ID you want your bot to add the slash command to
  @permissions.has_permissions(ban_members=True)
  async def ban(self, ctx, member: Option(discord.Member, "Member to ban", required=True), reason: Option(str, "Reason", default="No reason provided."), delete_message_days: Option(int, required=False)): # If a reason is a NoneType (none), it defaults to 'No reason provided.'
    await ctx.defer()
    if delete_message_days <= 7:
      delete_message_days = 7 # Discord doesn't allow messages older than 7 days to be deleted in this method, so we change it to 7 and move on
    if member == ctx.author:
      return await ctx.respond("You can't ban yourself.") #self explanatory 
    if member.top_role >= ctx.author.top_role: # checks to see if the user is trying to ban a user higher than them (e.g. Staff member trying to ban Management member)
      return await ctx.respond("You can't ban a user that's higher than you.")
    # creating an embed to send to the member
    embed = discord.Embed(color=discord.Colour.red(), description=f"You've been banned in {ctx.guild.name}!")
    embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon if ctx.guild.icon else "https://media.pocketgamer.biz/2021/5/110514/discord-new-logo-2021-r225x.jpg") # Now, this is a big thing: pycord changed the way the 'OBJECT.icon/avatar_url' works. it might throw an error if 'ctx.guild' doesn't have an icon; I recommend leaving it how it is if you're using pycord, if you're using discord.py, change '.icon' > '.icon_url'
    embed.add_field(name="Reason", value=reason)
    try:
      await member.send(embed=embed)
    except discord.Forbidden:
      pass # ignoring that the member couldn't be messaged
    try:
      await member.ban(reason=reason, delete_message_days=delete_message_days)
    except discord.Forbidden: # if you're using discord.py, use 'discord.errors.Forbidden' instead of 'discord.Forbiddn'; means the bot can't ban the user
      return await ctx.respond(f"Could not ban {member}; please make sure I have `Ban Members` permissions.")
    await ctx.respond(f"🔨 Banned `{member}`\n**Reason:** {reason}")

def setup(bot):
  bot.add_cog(Ban(bot))
