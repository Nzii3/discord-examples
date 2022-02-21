# MAIN BOT FILE
import discord
from discord.ext import commands

PREFIX = "!" # you can change this to what you want (e.g. '>'; '-'; '?'; '$')

client = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())
# Now, there are 3 things you can do to make your bot:
# discord.Bot > slash commands, other UI stuff (buttons, selects, context commands/apps, modals), events
# discord.Client > only events (@client.event, @commands.Cog.listener)
# commands.Bot > everything that a bot can have (everything mentioned above)

### NOTE: IF YOU ARE USING 'commands.Bot' WITH A VERIFIED BOT, AT THE START OF APRIL:
### YOU WILL NEED TO APPLY FOR THE 'message content intent' TO BE ABLE TO USE NORMAL PREFIX COMMANDS

@client.event
async def on_ready():
  # if you decide to do persistent views, do 'client.add_view(MyClass())' before printing ready
  # do this so you don't accidently try to run commands while it's adding views
  print(f'{client.user} is ready!')


TOKEN = "put your token here" # put your bot's token in the string, you can get your bot's token from the Developer Portal
client.run(TOKEN)
