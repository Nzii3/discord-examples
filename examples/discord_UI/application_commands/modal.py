import discord
from discord.ext import commands
from discord.commands import slash_command

### NOTE: MODALS CAN'T BE INVOKED FROM MESSAGE COMMANDS
### THEY HAVE TO BE INVOKED FROM A UI INTERACTION
### HAS TO BE INVOKED FROM: SLASH COMMANDS, BUTTON, SELECTS, CONTEXT COMMANDS

class MyModal(discord.ui.Modal):
  def __init__(self):
    super.__init__("My app title") # setting the app title/name
    self.add_item(discord.ui.InputText(label="My app question", placeholder="My placeholder", min_length=1, max_length=100))
    # Optional arguments:
    # 'required' (default = True)
    # 'style' discord.InputTextStyle (default = short)
    # 'placeholder' (default = None)
    # 'value' this is the test that is already in the field (default = None)
    # 'min_length' inherits from 'style' kwarg
    # 'max_length' inherits from 'style' kwarg (default = 4000 - I think)
    async def mycallback(self, interaction: discord.Interaction):
      embed = discord.Embed(color=discord.Colour.blurple(), title="Your Application Results")
      for item in self.children:
        embed.add_field(name=item.label, value=item.value)
      await interaction.response.send_message(embed=embed, ephemeral=True) # sending all of our answers in an embed that's hidden

class MyModalButton(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=60.0)
  async def on_timeout(self):
    for child in self.children:
      child.disabled = True
    await self.message.edit(content="Timeout exceeded", view=self)
  
  @discord.ui.button(style=discord.ButtonStyle.grey, label="Application")
  async def mycallback(self, button, interaction):
    # please note that you CAN'T defer here, just a Discord thing unfortunately :(
    await interaction.response.send_modal(MyModal())

# somewhere else
class MyModalCommand(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command()
  async def sendmodal(self, ctx):
    await ctx.reply(view=MyModalButton())

  @slash_command(name="sendmodal", guild_ids=[123456789]) # replace '123...' with your guild ID
  async def send_modal_slash(self, ctx):
    await ctx.interaction.response.send_modal(MyModal())
  
def setup(bot):
  bot.add_cog(MyModalCommand(bot))