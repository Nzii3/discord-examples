import discord
from discord.ext import commands

from discord.commands import slash_command, Option, permissions

class Say(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

### PREFIX COMMAND
  @commands.command()
  @commands.has_guild_permissions(manage_messages=True)
  async def say(self, ctx, *, message: str=None):
    await ctx.trigger_typing()
    if message is None:
      return await ctx.reply("Please provide a message to say.")
    await ctx.message.delete()
    await ctx.send(message, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False))
    # NOTE: passing in 'allowed_mentions' in this way, doesn't allow the author to ping roles or everyone using the bot (prevents nukes and bot raids while using the command)


### SLASH COMMAND
  @slash_command(name="say", guild_ids=[123456789]) # replace '123...' with your guild's id
  @permissions.has_role(123456789) # repalce '123...' with the role you want to allow to use the slash command
  #@commands.has_guild_permissions(manage_messages=True)
  # This works too ^ but it will allow all users to use the command but it won't run the command callback and raise an error that they don't have permissions
  async def _say(self, ctx, message: Option(str, "The message to say", required=True)):
    await ctx.defer(ephemeral=True)
    await ctx.channel.send(message, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False))
    await ctx.respond("Sent message!", ephemeral=True)

def setup(bot):
  bot.add_cog(Say(bot))
