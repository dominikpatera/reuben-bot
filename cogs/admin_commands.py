import discord
from discord.ext import commands
from discord.utils import get

from classes.channels import Channels
from classes.roles import Roles


class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.channels = Channels().getChannels()
        self.roles = Roles()
        self.main_roles = self.roles.getMainRoles()

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)

        rules = self.client.get_channel(self.channels['firstSteps']['rules'])

        message = ''
        private_message = f'⚠️ **BYL SI VAROVÁN** ⚠️\n\n{ctx.message.author.mention} tě varoval'
        if reason is None:
            message = f'⚠️ {ctx.message.author.mention} varoval {member.mention}.'
            private_message = private_message + '. 🚨'
        else:
            message = f'⚠️ {ctx.message.author.mention} varoval {member.mention} za {reason}.'
            private_message = private_message+f' za {reason}. 🚨'
        private_message = private_message + \
            f'\n\nMěl by sis znovu přečíst {rules.mention} a dodržovat je. 😊\n\nReuben\n*oink*'

        channel = self.client.get_channel(
            self.channels['public']['discord'])  # discord
        await channel.send(message)
        await member.send(private_message)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)

        roles = [r.id for r in member.roles]
        guild = member.guild

        for r in roles:
            if r != self.roles['main']['everyone']['id']:  # everyone
                role = get(guild.roles, id=r)
                await member.remove_roles(role)

        role = get(guild.roles, id=self.roles['main']['banned']['id'])

        await member.add_roles(role)

        info = self.client.get_channel(self.channels['banned']['info'])
        banappeals = self.client.get_channel(
            self.channels['banned']['ban-appeals'])

        message = ''
        private_message = f'🛑 **BYL SI ZABANOVÁN** 🛑\n\n{ctx.message.author.mention} tě zabanoval'
        if reason is None:
            message = f'🛑 {ctx.message.author.mention} zabanoval {member.mention}.'
            private_message = private_message + '. ❌'
        else:
            message = f'🛑 {ctx.message.author.mention} zabanoval {member.mention} za {reason}.'
            private_message = private_message+f' za {reason}. ❌'
        private_message = private_message + \
            f'\n\nMěl by sis přečíst {info.mention} a napsat své odvolání do {banappeals.mention}.\n\nReuben\n*oink*'

        channel = self.client.get_channel(
            self.channels['public']['discord'])  # discord
        await channel.send(message)
        await member.send(private_message)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)

        guild = member.guild

        # banned
        await member.remove_roles(get(guild.roles, id=self.roles['main']['banned']['id']))

        rules = self.client.get_channel(self.channels['firstSteps']['rules'])
        welcome = self.client.get_channel(
            self.channels['firstSteps']['welcome'])
        pickrole = self.client.get_channel(
            self.channels['firstSteps']['pick-role'])

        message = ''
        private_message = f'💚 **BYL SI ODBANOVÁN** 💚\n\n{ctx.message.author.mention} tě odbanoval'
        if reason is None:
            message = f'💚 {ctx.message.author.mention} odbanoval {member.mention}.'
            private_message = private_message + '. ✅'
        else:
            message = f'💚 {ctx.message.author.mention} odbanoval {member.mention} za {reason}.'
            private_message = private_message + f' za {reason}. ✅'
        private_message = private_message + \
            f'\n\nNezapomeň si přečíst {rules.mention},' + \
            f' ověřit se ✅ ve {welcome.mention} (pokud si již byl ověřen, tak musíš znovu zaškrtnout emoji ✅) a vybrat roli v {pickrole.mention} podle tvých zájmů 👍!\n\nReuben\n*oink*'

        channel = self.client.get_channel(
            self.channels['public']['discord'])  # discord
        await channel.send(message)
        await member.send(private_message)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)

    @commands.command(aliases=['bot_message', 'send'])
    @commands.has_role(Roles().getMainRoles()['main']['admin']['id'])  # admin
    async def message_bot(self, ctx, channel: discord.TextChannel, *, text=None):
        await ctx.channel.purge(limit=1)
        await channel.send(f'{text}')

    @commands.command(aliases=['edit'])
    @commands.has_role(Roles().getMainRoles()['main']['admin']['id'])  # admin
    async def edit_message(self, ctx, message: discord.Message, *, text=None):
        await ctx.channel.purge(limit=1)
        await message.edit(content=text)

    @commands.command(aliases=['react'])
    @commands.has_role(Roles().getMainRoles()['main']['admin']['id'])  # admin
    async def react_to_message(self, ctx, message: discord.Message, *, reaction):
        await ctx.channel.purge(limit=1)
        await message.add_reaction(reaction)

    @commands.command(aliases=['unreact'])
    @commands.has_role(Roles().getMainRoles()['main']['admin']['id'])  # admin
    async def unreact_to_message(self, ctx, message: discord.Message, *, reaction):
        await ctx.channel.purge(limit=1)
        await message.clear_reaction(reaction)

    @commands.command(aliases=['addrole'])
    @commands.has_role(Roles().getMainRoles()['main']['admin']['id'])  # admin
    async def add_role(self, ctx, member: discord.Member, *, role: discord.Role):
        await ctx.channel.purge(limit=1)
        await member.add_roles(role)
        message = f'🥰 Role {role.mention} was given to {member.mention}.'
        channel = self.client.get_channel(
            self.channels['public']['discord'])  # discord
        await channel.send(message)

    @commands.command(aliases=['removerole'])
    @commands.has_role(Roles().getMainRoles()['main']['admin']['id'])  # admin
    async def remove_role(self, ctx, member: discord.Member, *, role: discord.Role):
        await ctx.channel.purge(limit=1)
        await member.remove_roles(role)
        message = f'😢 Role {role.mention} was removed from {member.mention}.'
        channel = self.client.get_channel(
            self.channels['public']['discord'])  # discord
        await channel.send(message)


def setup(client):
    client.add_cog(AdminCommands(client))
