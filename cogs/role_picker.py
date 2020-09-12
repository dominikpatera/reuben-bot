import discord
import re
from discord.ext import commands
from discord.utils import get


class RolePicker(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.games = {
            "csgo": 753895813926879312,  # csgo
            "minecraftAnimated": 753896417059143710,  # minecraft
            "fortnite": 753938108311011451,  # fortnite
            "valorant": 753937040311189516,  # valorant
            "lol": 753939985849122847,  # league of legends
            "amongUs": 754045760588218560,  # among us
            "fallGuys": 753941469886283828,  # fall guys
            "tm": 753941437111992441,  # trackmania
            "wow": 753941499401470044  # wow
        }

        self.roles = {
            "✅": 753894111131467848,  # user
            "🎮": 754082767301640342,  # gamer
            "🚀": 754082846104354906,  # tech
            "🎨": 754088046328021003,  # developer/designer
            "📖": 754101527672651835,  # study
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = payload.member.guild
        member = payload.member
        channel_id = payload.channel_id
        emoji = payload.emoji

        if channel_id == 753889477742690305:
            if emoji.name in self.games:
                role = get(guild.roles, id=self.games[emoji.name])
                await member.add_roles(role)
        elif channel_id == 753887103976472646 or channel_id == 754090438314557573:
            if emoji.name in self.roles:
                role = get(guild.roles, id=self.roles[emoji.name])
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = discord.utils.find(
            lambda g: g.id == payload.guild_id, self.client.guilds)
        member = discord.utils.find(
            lambda m: m.id == payload.user_id, guild.members)
        channel_id = payload.channel_id
        emoji = payload.emoji

        if channel_id == 753889477742690305:
            if emoji.name in self.games:
                role = get(guild.roles, id=self.games[emoji.name])
                await member.remove_roles(role)
        elif channel_id == 754090438314557573:
            if emoji.name in self.roles:
                role = get(guild.roles, id=self.roles[emoji.name])
                await member.remove_roles(role)


def setup(client):
    client.add_cog(RolePicker(client))
