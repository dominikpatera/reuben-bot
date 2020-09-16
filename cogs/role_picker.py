import discord
from discord.ext import commands
from discord.utils import get
from classes.channels import Channels
from classes.roles import Roles


class RolePicker(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.channels = Channels().getChannels()
        self.roles = Roles()
        self.main_roles = self.roles.getMainRoles()
        self.games_roles = self.roles.getGamesRoles()
        self.interests_roles = self.roles.getInterestsRoles()

        self.games_keys = self.games_roles.keys()
        self.interests_keys = self.interests_roles.keys()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = payload.member.guild
        member = payload.member
        channel_id = payload.channel_id
        emoji = payload.emoji

        if channel_id == self.channels['games']['pick-games']:  # pick games
            for game in self.games_keys:
                if emoji.name in self.games_roles[game]['emoji']:
                    role = get(guild.roles, id=self.games_roles[game]['id'])
                    await member.add_roles(role)
            # pick roles and welcome
        elif channel_id in [self.channels['firstSteps']['pick-role'], self.channels['firstSteps']['welcome']]:
            for interest in self.interests_keys:
                if emoji.name in self.interests_roles[interest]['emoji']:
                    role = get(
                        guild.roles, id=self.interests_roles[interest]['id'])
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = discord.utils.find(
            lambda g: g.id == payload.guild_id, self.client.guilds)
        member = discord.utils.find(
            lambda m: m.id == payload.user_id, guild.members)
        channel_id = payload.channel_id
        emoji = payload.emoji

        if channel_id == self.channels['games']['pick-games']:  # pick games
            for game in self.games_keys:
                if emoji.name in self.games_roles[game]['emoji']:
                    role = get(guild.roles, id=self.games_roles[game]['id'])
                    await member.remove_roles(role)
            # pick roles and welcome
        elif channel_id == self.channels['firstSteps']['pick-role']:  # pick roles
            for interest in self.interests_keys:
                if emoji.name in self.interests_roles[interest]['emoji']:
                    role = get(
                        guild.roles, id=self.interests_roles[interest]['id'])
                    await member.remove_roles(role)


def setup(client):
    client.add_cog(RolePicker(client))
