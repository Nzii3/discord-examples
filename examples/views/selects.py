import discord
from discord.ext import commands

### PLEASE READ 'discord-examples/examples/views/README.md' before continuing

class MySelectView(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=30.0)

  @discord.ui.select(options=[discord.SelectOption(label="Red", description="Your favourite colour is red", emoji="🟥"), discord.SelectOption(label="Green", description="Your favourite colour is green", emoji="🟩"), discord.SelectOption(label="Blue", description="Your favourite colour is blue", emoji="🟦")], placeholder="My placeholder", min_values=1, max_values=1)
  # NOTE: 'max_values' is the maximum amount of selections a user can have; 'min_values' is the minimum values a user can select
  #   - these have to be a float/int object when set
  # NOTE: You can pass in 'custom_id="..."' if you need to above
  async def mycallback(self, select, interaction: discord.Interaction):
    await interaction.response.send_message(f"Your favorite color is {select.values[0]}") # 'select.values' is a list of the values selected

# somewhere else

class MyCog(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.command()
  async def colors(self, ctx):
    view = MySelectView()
    await ctx.send(content="Select your favorite color!", view=view)

def setup(bot: commands.Bot):
  bot.add_cog(MyCog(bot))