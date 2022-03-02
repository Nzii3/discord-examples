import discord
from discord.ext import commands

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


### TO DO:
# Button that invokes the modal
# Slash command that invokes the modal
# Select that invokes the modal
# Context command that invokes the modal


