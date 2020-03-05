import random
import requests
from discord.ext import commands
from lamb import memory


class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, max_number=""):
        """Roll a random number between one and inputted number"""
        if max_number == "":
            await ctx.message.delete()
            await ctx.send(
                f'{ctx.message.author.mention} - usage: {memory["command_prefix"]}roll <max_number>', delete_after=10)
            return
        with ctx.typing():
            try:
                roll = random.randint(1, int(max_number))
            except TypeError:
                await ctx.message.delete()
                await ctx.send(f'{ctx.message.author.mention} - {max_number} is not a number.', delete_after=10)
                return

        await ctx.send(f'*{ctx.message.author.mention} Rolls a {roll}*  (1-{max_number})')

    @commands.command()
    async def insult(self, ctx, username):
        """Insult a member of your guild, free of charge"""
        with ctx.typing():
            req = requests.get("https://insult.mattbas.org/api/insult")
            data = req.text
        await ctx.send(f'{username} {data}')


def setup(bot):
    bot.add_cog(GeneralCommands(bot))
