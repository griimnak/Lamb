from discord.ext import commands

from lamb.helpers import regex, re
from lamb.ytdl import YTDLSource


class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def summon(self, ctx):
        """Summons lamb to the summoner's voice channel"""
        channel = ctx.message.author.voice.channel  # get voice channel of summoner
        await channel.connect()  # connect to channel

    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():  # if bot is playing
            voice_client.stop()  # stop bot audio stream

    @commands.command()
    async def play(self, ctx, url):
        """[link] Play the audio of a valid youtube url"""
        # test url
        raw_url = re.match(regex, url)
        if raw_url is None:
            await ctx.send(f'`{url}` is not a valid youtube url.')
        else:
            server = ctx.message.guild
            voice_channel = server.voice_client

            async with ctx.typing():
                player = await YTDLSource.from_url(url, loop=self.bot.loop)
                ctx.message.guild.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            await ctx.send('playing: {}'.format(player.title))

    @commands.command()
    async def dismiss(self, ctx):
        """Dismiss lamb from the server's voice channels"""
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()


def setup(bot):
    bot.add_cog(MusicCommands(bot))
