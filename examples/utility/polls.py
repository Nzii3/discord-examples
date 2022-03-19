import discord
from discord.ext import commands
from datetime import datetime
from discord.commands import slash_command, Option, permissions

class Polls(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

### PREFIX COMMAND
  @commands.command()
  @commands.has_guild_permissions(manage_guild=True)
  async def poll(self, ctx, poll: str, *, channel: discord.TextChannel=None):
    await ctx.message.delete()
    await ctx.trigger_typing()
    if channel is None:
      channel = ctx.channel
    embed = discord.Embed(title=poll, color=discord.Colour.blurple(), timestamp=datetime.utcnow())
    embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
    embed.set_footer(text="Use the reactions below to vote")
    reactions = ['✅', '❌']
    message = await ctx.send(embed=embed)
    for r in reactions:
      await message.add_reaction(r)

### SLASH COMMAND
  @slash_command(name="poll")
  @permissions.has_guild_permissions(manage_messages=True)
  async def _poll(self, ctx, poll: Option(str, required=True), *, channel: Option(discord.TextChannel, require=False)):
    await ctx.defer(ephemeral=True)
    if channel is None:
      channel = ctx.channel
    embed = discord.Embed(title=poll, color=discord.Colour.blurple(), timestamp=datetime.utcnow())
    embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar)
    embed.set_footer(text="Use the reactions below to vote")
    reactions = ['✅', '❌']
    message = await ctx.channel.send(embed=embed)
    await ctx.respond(f"✅ Embed sent to {channel.mention}!", ephemeral=True)
    for r in reactions:
      await message.add_reaction(r)

def setup(bot):
  bot.add_cog(Polls(bot))