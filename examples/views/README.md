# Discord Views

There is something called the `message component family`. This family consists of buttons, selects, context menus, etc. This "family" are component UIs that can be on messages.

## Subclassing views

To easily subclass a view, follow this format and change the stuff that you need:
  - **This is mainly covered in [`discord-examples/examples/views/buttons.py`](https://github.com/Nziie3/discord-examples/blob/main/examples/views/buttons.py)**
```py
class MyView(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=60)

  ### OPTIONAL: async def on_timeout(self)
  #    - Check the 'discord-examples/examples/views/buttons.py' file to see 

  ### OPTIONAL: async def interaction_check(self, interaction: discord.Interaction)

  @discord.ui.[button|select](...) # remove the [] and '|' then choose what you want to add to your view: button or select
  async def mycallback(self, [button select], interaction: discord.Interaction): # remember to use remove the [] and pick what you want: button or select as one or the other needs to be passed
    # DO YOUR STUFF HERE
```

## Persistent Views
When you subclass views (and even adding a timeout), the view will timeout after a certain period of time and will stop working when you restart your bot (goes offline then online). So to prevent this, the py-cord developers have been very nice to add a way we can not have it stop working. 

**When you're creating a persistent view, you're gonna need to set the timeout of the view itself or it's components to `None`, as they can't have a timeout. The components (buttons, selects, etc) are also going to `NEED A CUSTOM_ID. YOU CAN SET THS CUSTOM_ID TO ANYTHING YOU WANT, IT JUST HAS TO HAVE IT.`**
```py
# MY VIEW CODE
class MyView(discord.ui.View):
...
...
# MAIN FILE:

client = commands.Bot(...)

@client.event
async def on_ready():
  client.add_view(MyView())
  # stuff
```
