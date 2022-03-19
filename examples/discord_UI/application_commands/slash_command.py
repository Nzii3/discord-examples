### REQUIRED IMPORTS
import discord
from discord.ext import commands
from discord.commands import slash_command, permissions, Option

class SlashCommandCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @slash_command(name="slash_command_normal", description="This is my normal slash command", guild_ids=[123456789])
  # NOTE: MAKE SURE TO REPLACE '123...' IN guild_ids WITH YOUR *OWN* GUILD ID, YOUR BOT HAS TO BE IN THE SERVER
  # IF THE BOT ISNT IN THE SERVER THAT YOU ARE INSERTING THE GUILD ID FOR, IT WILL RAISE AN ERROR AND YOUR BOT WON'T START
  async def slash_command_normal(self, ctx):
    await ctx.defer() # deferring the response, this makes the bot show as '{bot_name} is thinking...'
    await ctx.respond("Hello")


  @slash_command(name="slash_command_hidden", description="This is my hidden slash command", guild_ids=[123456789])
  async def slash_command_hidden(self, ctx):
    await ctx.defer(ephemeral=True) # ephemeral makes the response hidden to only the author
    await ctx.respond("Hello, this is a hidden message", ephemeral=True)

  @slash_command(name="slash_command_option", description="This is my slash command with an option", guild_ids=[123456789])
  async def slash_command_option(self, ctx, myvalue: Option(str, "This is my option description, optional", required=True)): # by default, the option is required
    await ctx.defer()
    await ctx.respond(f"You responded with {myvalue}!")

  @slash_command(name="slash_command_memberoption", description="This slash command is a member option", guild_ids=[123456789])
  async def slash_command_memberoption(self, ctx, member: Option(discord.Member, "Member object", required=True)):
    await ctx.defer()
    await ctx.respond(f"You provided {member} ({member.id}) as a member object!")

  @slash_command(name="slash_command_preset", description="This slash command has preset options", guild_ids=[123456789])
  async def slash_command_preset(self, ctx, choice: Option(str, "Preset options", choices=["Option 1", "Option 2", "Option 3"], required=True)):
    await ctx.defer()
    await ctx.respond(f"Your option that you selected is {choice}!")

def setup(bot):
  bot.add_cog(SlashCommandCog(bot))
