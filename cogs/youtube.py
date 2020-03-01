from discord.ext import commands

from lamb.helpers import regex, re
from lamb.ytdl import YTDLSource
from lamb import memory


class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, url):
        """Play the audio of a valid youtube url"""
        await ctx.message.delete()

        # test url
        raw_url = re.match(regex, url)
        if raw_url is None:
            await ctx.send(f'`{url}` is not a valid youtube url.')
        else:
            voice_channel = ctx.message.guild.voice_client

            if voice_channel is None:
                await ctx.message.author.voice.channel.connect()
            elif voice_channel.is_playing():
                await ctx.send(f'{ctx.message.author.mention} Wait for the current song to finish, or use `{memory["command_prefix"]}stop`.', delete_after=10)
                return

            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop)
                ctx.message.guild.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            await ctx.send(f'Now Playing: `{player.title}` \nSource: {url} ({ctx.message.author.mention})')

    @commands.command()
    async def stop(self, ctx):
        """Stop playing current audio stream"""
        await ctx.message.delete()

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            voice_client.stop()  # stop bot audio stream

    @commands.command()
    async def dismiss(self, ctx):
        """Dismiss lamb from the server's voice channels"""
        await ctx.message.delete()

        voice_client = ctx.message.guild.voice_client
        if voice_client is None:
            return

        with ctx.typing():
            await voice_client.disconnect()
        await ctx.send("See ya,", delete_after=3)


def setup(bot):
    bot.add_cog(MusicCommands(bot))
