from discord.ext import commands
from lamb import memory


class DebugCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def debug(self, ctx):
        """Returns the lamb.memory json object"""
        guilds = {}

        for guild in self.bot.guilds:
            guilds[guild.name] = guild.member_count

        msg = f'```js\n{memory}```'

        await ctx.send(msg)

    @commands.command()
    async def ping(self, ctx):
        """Returns bot.latency in ms"""
        await ctx.send(f'Pong! `{self.bot.latency}`')

    @commands.command()
    async def cmds(self, ctx):
        """Returns number of Cogs registered"""
        await ctx.send(f'`{len(self.bot.commands)}` including `help` command')


def setup(bot):
    bot.add_cog(DebugCommands(bot))
