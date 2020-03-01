# Lamb

Light ass Management Bot


A simple and lightweight all-purpose Discord bot created with discord.py

Total dependencies: <b>3</b>
###### youtube_dl, discord, pynacl


#### Current Features
&#10004; Locale system<br/>
&#10004; Config system<br/>
&#10004; Music streaming (like Rythm Bot)<br/>
&#10004; Clean and extendable bot structure <br/>

![Alt Text](https://github.com/griimnak/Lamb/blob/master/lamb/temp/Screenshot_117.png)

Prerequisites
------------
#### Windows
Install the latest stable build of `Python 3` from <a href="https://www.python.org/downloads/">python.org</a>.

Make sure `python` is recognized. Help article: <a href="https://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-7">here</a>

Download lamb as a zip and extract it to your Desktop.



#### Linux
Verify you are using `Python 3.6+`
```shell script
python -V
```
Clone this git repository
```shell script
git clone thisrepo
```

Installation
-------------
From within the directory you extracted, launch a command prompt (or terminal) and run the following command. 
```shell script
python -m pip install -r requirements.txt
```

Launching
-------------
Firstly, generate an application and retrieve your `bot token`. Help article: <a href="https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token">here</a>

Second, check out `settings/config.json` and paste your token into the `token=""` field.

You're now ready to launch lamb.
```shell script
python start.py
```
Alternatively if you're on Windows, you can launch lamb by double-clicking `winstart.bat`

To learn how to add your Discord bot to servers, <a href="https://github.com/jagrosh/MusicBot/wiki/Adding-Your-Bot-To-Your-Server">click here</a>

Coding Commands
--------------
Lamb is structured to be a perfect starting point for developing your own custom commands.

Visit the `discord.py` api documentation <a href="https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html">here</a>.

The main gist is this,
```python
from discord.ext import commands

class MyCustomCog(commands.Cog):
    """Every Cog starts like this."""
    def __init__(self, bot):
        self.bot = bot
``` 
Cogs (command groups) are placed in `cogs/`, this location can be changed in `settings/config.json`

Using the template above, you would start a custom command like so: (within class block)
```python
    @commands.command()
    async def ping(self, ctx):
        """These docstrings are used as descriptions when using !help"""
        await ctx.send("Pong!")
```

Final product:
```python
from discord.ext import commands

class MyCustomCog(commands.Cog):
    """Every Cog starts like this."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """These docstrings are used as descriptions when using !help"""
        await ctx.send("Pong!")
```

### Public Functions
Below are public accessible functions for use throughout the Bot

Accessing the Bot's memory and state data
```python
from lamb import memory 

print(memory) # memory of lamb instance
>>>> {'active': True, 'py_version': (3, 6), 'lamb_version': '0.0', 'token': '', 'command_prefix': '#', 'temp_dir': './lamb/temp/', 'cogs_dir': './cogs/', 'strings_locale': 'en_US', 'strings': {'greeting': 'Welcome to the server.', 'banned': '{user} has been banned from the server.'}}


# you can also set memory variables like so
memory["custom_var"] = "my custom value"
memory["command_prefix"] = "$" # updating a value
```

Serving
```python
import lamb as DiscordBot

DiscordBot.load_settings()
DiscordBot.serve_now()
```

Reloading the json settings file
```python
from lamb import load_settings

load_settings()
```

