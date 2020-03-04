import discord
from discord.ext import commands
from statistics import mode
from urllib import parse

from lamb.helpers import datetime_now
from lamb.lol import LoLTracker, LoLException
from lamb import memory


class LoLTrackerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = LoLTracker(memory["riot_api"]["token"])

    @staticmethod
    def print_lane(lane):
        """Pretty print lane"""
        if lane == 'BOTTOM':
            lane = 'Bot lane '
        if lane == 'TOP':
            lane = 'Top lane '
        if lane == 'MID':
            lane = 'Mid lane '
        if lane == 'JUNGLE':
            lane = 'Jungle '
        return lane

    @staticmethod
    def print_role(role):
        """Pretty print role"""
        if role == 'DUO_SUPPORT':
            role = ' Support'
        if role == 'DUO_CARRY':
            role = ' ADC'
        if role == 'SOLO':
            role = ' Solo'
        if role == 'NONE':
            role = ''
        return role

    @commands.command()
    async def lol(self, ctx, *summoner):
        """Return an overview of a summoner's league profile
        :param tuple summoner: summoner is a tuple because league allows spaces in names."""
        # await ctx.message.delete()

        try:
            data = self.api.get_basic_info(summoner)
        except LoLException:
            await ctx.message.delete()
            return await ctx.send(
                f'{ctx.message.author.mention} - Summoner `{" ".join(summoner)}` not found.', delete_after=10)

        # return history with account id from request above
        matches = self.api.get_draft_history(data["accountId"])

        roles = []
        champs = []
        lanes = []
        for match in matches:
            roles.append(matches[match]["role"])
            champs.append(matches[match]["champion"])
            lanes.append(matches[match]["lane"])

        role = mode(roles)
        lane = mode(lanes)
        champ_id = mode(champs)

        champ = self.api.get_champ_by_id(champ_id)
        mastery = self.api.get_mastery_data(data["id"], champ_id)
        ranked = self.api.get_ranked_data(data["id"])

        msg = f'''{ctx.message.author.mention} - Summoner found: `{data["name"]}`
Summoner level: `{data["summonerLevel"]}`
Region: `NA1` :flag_us:
Solo/Duo: `{ranked["solo/duo"]["tier"]} {ranked["solo/duo"]["rank"]}`
Flex: `{ranked["flex"]["tier"]} {ranked["flex"]["rank"]}`
Stats:(_last 20 games_)
Main role: `{self.print_role(role)} {self.print_lane(lane)}`
Main champion: `{champ}`
{champ} Mastery lvl `{mastery["championLevel"]}` `{mastery["championPoints"]}` points
[View on na.op.gg](https://na.op.gg/summoner/userName={parse.quote(data["name"])})'''

        with ctx.typing():
            embed = discord.Embed(colour=discord.Colour(0x2b7e4c), description=msg)

            embed.set_image(url=f'{self.api.cdn_url}/img/champion/splash/{champ.replace(" ","")}_0.jpg')

            embed.set_thumbnail(url=f'{self.api.cdn_url}/{self.api.lol_ver}/img/profileicon/{data["profileIconId"]}.png')
        await ctx.send("", embed=embed)


def setup(bot):
    if memory["riot_api"]["token"] == "":
        print(f'[{datetime_now()}] (LoLTracker): Token not set, commands are disabled.')
        return
    print(f'[{datetime_now()}] (LoLTracker): RiotAPI token provided: {memory["riot_api"]["token"]}')
    bot.add_cog(LoLTrackerCommands(bot))
