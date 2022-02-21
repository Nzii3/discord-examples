# REQUIRED IMPORTS
from email.policy import default
import discord
from discord.ext import commands
import re
from datetime import timedelta

# OPTIONAL IMPORTS
from discord.commands import slash_command, Option, permissions

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter): # this is a time converter, it will basically convert humanized-time into seconds then return it so datetime.timedelta can do it's thing
  async def convert(self, ctx, argument):
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for v, k in matches:
      try:
        time += time_dict[k]*float(v)
      except KeyError:
        raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
      except ValueError:
        raise commands.BadArgument("{} is not a number!".format(v))
    return time

class Timeout(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

### PREFIX COMMAND ###
  @commands.command(aliases=["mute"])
  @commands.has_permissions(moderate_members=True)
  async def timeout(self, ctx, member: discord.Member, time: TimeConverter, *, reason="No reason provided"):
    await ctx.trigger_typing()
    if time > 604800:
      return await ctx.reply(f"You cannot time someone out for longer than a week; Discord limitations :(")
    if member == ctx.author:
      return await ctx.reply("You can't mute yourself.") #self explanatory 
    if member.top_role >= ctx.author.top_role: # checks to see if the user is trying to ban a user higher than them (e.g. Staff member trying to ban Management member)
      return await ctx.reply("You can't mute a user that's higher than you.")
    try:
      await member.timeout_for(duration=timedelta(seconds=time), reason=reason)
    except discord.Forbidden:
      return await ctx.reply("It seems like I can't timeout that member.")
    timeout_till = f"<t:{int(member.communication_disabled_until.timestamp())}>"
    await ctx.reply(f"Muted `{member}` until {timeout_till}.")

### SLASH COMMAND ###

  @slash_command()
  @permissions.has_permissions(moderate_members=True)
  async def timeout(self, ctx, member: Option(discord.Member, "Member to timeout", required=True), time: TimeConverter, reason: Option(str, "Reason", required=False, default="No reason provided.")):
    await ctx.defer()
    if time > 604800:
      return await ctx.interaction.followup.send(f"You cannot time someone out for longer than a week; Discord limitations :(")
    if member == ctx.author:
      return await ctx.interaction.followup.send("You can't mute yourself.") #self explanatory 
    if member.top_role >= ctx.author.top_role: # checks to see if the user is trying to ban a user higher than them (e.g. Staff member trying to ban Management member)
      return await ctx.interaction.followup.send("You can't mute a user that's higher than you.")
    try:
      await member.timeout_for(duration=timedelta(seconds=time), reason=reason)
    except discord.Forbidden:
      return await ctx.interaction.followup.send("It seems like I can't timeout that member.")
    timeout_till = f"<t:{int(member.communication_disabled_until.timestamp())}>"
    await ctx.interaction.followup.send(f"Muted `{member}` until {timeout_till}.")

def setup(bot: commands.Bot):
  bot.add_cog(Timeout(bot))
    
