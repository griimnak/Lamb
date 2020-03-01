import os
from discord.ext import commands

from .bot import memory, __version__, __author__
from .helpers import load_settings, datetime_now


def serve_now():
    """Creates bot instance after lamb.load_settings"""
    if memory["token"] == "":
        exit("Please supply your token to settings/config.json")
    print(f'[{datetime_now()}] Token provided: {memory["token"]}')

    bot = commands.Bot(command_prefix=memory["command_prefix"])

    # Load all cogs
    for filename in os.listdir(memory["cogs_dir"]):
        if filename.endswith('.py') and not filename.endswith('__init__.py'):
            bot.load_extension(f'{memory["cogs_dir"][2:-1]}.{filename[:-3]}')

    # Base
    @bot.command()
    async def load(ctx, extension):
        """Loads a Cog extension"""
        bot.load_extension(f'{memory["cogs_dir"][2:-1]}.{extension}')

    @bot.command()
    async def unload(ctx, extension):
        """Unloads an active Cog extension"""
        bot.unload_extension(f'{memory["cogs_dir"][2:-1]}.{extension}')

    @bot.event
    async def on_ready():
        print(f'[{datetime_now()}] Login successfull!')
        print(f'[{datetime_now()}] SESSION: {bot.user}')

        server_count = 0
        server_names = []
        async for server in bot.fetch_guilds(limit=150):
            server_count += 1
            server_names.append(f'{server.name}[{server.id}]')

        print(f'[{datetime_now()}] SERVERS: ({server_count}) {", ".join(server_names)}')

    bot.run(memory["token"])
