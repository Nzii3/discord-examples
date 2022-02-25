# REQUIRED IMPORTS
import discord
from discord.ext import commands

# OPTIONAL IMPORTS
from discord.commands import slash_command, Option

class RoleInfo(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

### PREFIX COMMAND

  @commands.command()
  async def roleinfo(self, ctx, role: discord.Role): # 'discord.Role' can take in a role's name, ID, or mention
    await ctx.trigger_typing()
    info = discord.Embed(color=role.color, description=role.mention)
    info.set_author(name=role.name, icon_url=ctx.guild.icon if ctx.guild.icon else "https://media.pocketgamer.biz/2021/5/110514/discord-new-logo-2021-r225x.jpg")
    info.add_field(name="Name", value=role.name, inline=True)
    info.add_field(name="Created", value=f"{discord.utils.format_dt(role.created_at, style='F')} ({discord.utils.format_dt(role.created_at, style='R')})", inline=True) # 'inline' makes the fields in line in the embed, by default it's False
    info.add_field(name="Members", value=len(role.members), inline=True)
    info.add_field(name="Color", value=str(role.color), inline=True)
    info.add_field(name="Mentionable", value=str(role.mentionable), inline=True)
    info.add_field(name="Hoisted", value=str(role.hoist), inline=True)
    info.add_field(name="Managed", value=str(role.managed), inline=True)
    return await ctx.reply(embed=info, mention_author=False)

### SLASH COMMAND

  @slash_command(guild_ids=[123456789]) # replace '123...' with your guild ID
  async def roleinfo(self, ctx, role: Option(discord.Role, required=True)):
    await ctx.defer()
    info = discord.Embed(color=role.color, description=role.mention)
    info.set_author(name=role.name, icon_url=ctx.guild.icon if ctx.guild.icon else "https://media.pocketgamer.biz/2021/5/110514/discord-new-logo-2021-r225x.jpg")
    info.add_field(name="Name", value=role.name, inline=True)
    info.add_field(name="Created", value=f"{discord.utils.format_dt(role.created_at, style='F')} ({discord.utils.format_dt(role.created_at, style='R')})", inline=True) # 'inline' makes the fields in line in the embed, by default it's False
    info.add_field(name="Members", value=len(role.members), inline=True)
    info.add_field(name="Color", value=str(role.color), inline=True)
    info.add_field(name="Mentionable", value=str(role.mentionable), inline=True)
    info.add_field(name="Hoisted", value=str(role.hoist), inline=True)
    info.add_field(name="Managed", value=str(role.managed), inline=True)
    return await ctx.respond(embed=info)

def setup(bot: commands.Bot):
  bot.add_cog(RoleInfo(bot))