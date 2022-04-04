
### NOTE: This is a warning command without a database, you can use MongoDB (what I use) or Sqlite to store your warning data

# REQUIRED IMPORTS
import discord
from discord.ext import commands

# OPTIONAL IMPORTS
from discord.commands import slash_command, Option, permissions

class Warn(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  
  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def warn(self, ctx, member: discord.Member, *, reason: str): # 'reason' is now a required argument
    await ctx.trigger_typing()
    if ctx.author == member:
      return await ctx.reply("You can't warn yourself.")
    if reason is None: # let's handle this so it doesn't throw an error
      return await ctx.reply("Please provide a reason for issuing a warning.")
    if member.top_role >= ctx.author.top_role: # checks to see if the user is trying to warn a user higher than them (e.g. Staff member trying to ban Management member)
      return await ctx.reply("You can't mute a user that's higher than you.")
    warning_embed = discord.Embed(color=discord.Colour.red(), description=f"You've been warned in {ctx.guild.name}!")
    warning_embed.add_field(name="Moderator", value=f"{ctx.author} (ID: {ctx.author.id})") # Shows the moderator to the warned user, optional
    warning_embed.add_field(name="Reason", value=reason, inline=True)
    warning_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon if ctx.guild.icon else "https://media.pocketgamer.biz/2021/5/110514/discord-new-logo-2021-r225x.jpg") # remember to add this if your server doesn't have an icon
    try:
      await member.send(embed=warning_embed)
    except discord.Forbidden:
      return await ctx.reply("Could not message that member about their warning.") # we're going to return this because if the member can't be messaged, there is not point of making it successfull
                                                                                   # as the whole point of warning someone is to DM them
    await ctx.reply(f"⚠  Successfully warned **{member}**!")
    # Quick Note: if you get an error: "'ctx' has no attribute 'reply'", try changing 'ctx.reply' to 'ctx.message.reply'.
    # if this still doesn't work, go to the pycord support server: discord.gg/pycord

  @slash_command(guild_ids=[123456789]) # replace '123...' with your server's ID
  @permissions.has_permissions(manage_messages=True)
  async def warn(self, ctx, member: Option(discord.Member, "The member to warn", required=True), reason: Option(str, "Reason", required=True)): # reason is now a required argument\
    await ctx.defer() # if you do want to make this an ephemeral (hidden) defer, pass in: 'ephemeral=True' then to followups, pass the same thing in
    if ctx.author == member:
      return await ctx.respond("You can't warn yourself.")
    if member.top_role >= ctx.author.top_role: # checks to see if the user is trying to warn a user higher than them (e.g. Staff member trying to ban Management member)
      return await ctx.respond("You can't mute a user that's higher than you.")
    warning_embed = discord.Embed(color=discord.Colour.red(), description=f"You've been warned in {ctx.guild.name}!")
    warning_embed.add_field(name="Moderator", value=f"{ctx.author} (ID: {ctx.author.id})") # Shows the moderator to the warned user, optional
    warning_embed.add_field(name="Reason", value=reason, inline=True)
    warning_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon if ctx.guild.icon else "https://media.pocketgamer.biz/2021/5/110514/discord-new-logo-2021-r225x.jpg") # remember to add this if your server doesn't have an icon
    try:
      await member.send(embed=warning_embed)
    except discord.Forbidden:
      return await ctx.interaction.followup.send("Could not message that member about their warning.")
    await ctx.respond(f"⚠  Successfully warned **{member}**!")

def setup(bot):
  bot.add_cog(Warn(bot))
