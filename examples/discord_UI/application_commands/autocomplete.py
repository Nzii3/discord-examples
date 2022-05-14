import discord
from discord.ext import commands
from discord.commands import slash_command, permissions, Option

class SlashCommandAutocomplete(commands.Cog):
  # Discord's slash command autocomplete feature allows developers to
  # change a slash command option's choices for a specific user, channel, guild, etc.
  def __init__(self, bot):
    self.bot = bot
  
  # creating autocomplete function
  async def my_autocomplete(ctx: discord.AutocompleteContext):# NOTE: YOU MUST RETURN A LIST TYPE
    if ctx.channel.name == "special-channel":
      return ['Special Channel', 'Channel is special']
    if ctx.author == ctx.guild.owner:
      return ['Server owner', "You're the owner"]
    if ctx.guild.name == "nziie is cool":
      return ['Nziie is cool', 'Nziie is very cool!']

  #NOTE: autocomplete only works with slash commands
  @slash_command(name="autocomplete_example", guild_ids=[123456789]) # REPLACE GUILD IDS
  async def autocomplete_example(self, ctx, autocomplete: Option(str, required=True, autocomplete=my_autocomplete)): # don't call [()] the function
    await ctx.defer()
    await ctx.respond(str(autocomplete))

def setup(bot):
  bot.add_cog(SlashCommandAutocomplete(bot))