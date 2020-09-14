import discord
from discord.ext import commands
from discord.utils import get


class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)

        rules = self.client.get_channel(753919822823292988)

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

        channel = self.client.get_channel(753907336497725470)  # discord
        await channel.send(message)
        await member.send(private_message)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)

        roles = [r.id for r in member.roles]
        guild = member.guild

        for r in roles:
            if r != 753886874208174081:  # everyone
                role = get(guild.roles, id=r)
                await member.remove_roles(role)

        role = get(guild.roles, id=754103336243822683)

        await member.add_roles(role)

        info = self.client.get_channel(754286659436281887)
        banappeals = self.client.get_channel(754104965949030504)

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

        channel = self.client.get_channel(753907336497725470)  # discord
        await channel.send(message)
        await member.send(private_message)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)

        guild = member.guild

        # banned
        await member.remove_roles(get(guild.roles, id=754103336243822683))

        rules = self.client.get_channel(753919822823292988)
        welcome = self.client.get_channel(753887103976472646)
        pickrole = self.client.get_channel(754090438314557573)

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

        channel = self.client.get_channel(753907336497725470)  # discord
        await channel.send(message)
        await member.send(private_message)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)

    @commands.command(aliases=['bot_message', 'send'])
    @commands.has_role(753889013257207839)  # admin
    async def message_bot(self, ctx, channel: discord.TextChannel, *, text=None):
        await ctx.channel.purge(limit=1)
        await channel.send(f'{text}')

    @commands.command(aliases=['edit'])
    @commands.has_role(753889013257207839)  # admin
    async def edit_message(self, ctx, message: discord.Message, *, text=None):
        await ctx.channel.purge(limit=1)
        await message.edit(content=text)

    @commands.command(aliases=['react'])
    @commands.has_role(753889013257207839)  # admin
    async def react_to_message(self, ctx, message: discord.Message, *, reaction):
        await ctx.channel.purge(limit=1)
        await message.add_reaction(reaction)

    @commands.command(aliases=['unreact'])
    @commands.has_role(753889013257207839)  # admin
    async def unreact_to_message(self, ctx, message: discord.Message, *, reaction):
        await ctx.channel.purge(limit=1)
        await message.clear_reaction(reaction)

    @commands.command(aliases=['addrole'])
    @commands.has_role(753889013257207839)  # admin
    async def add_role(self, ctx, member: discord.Member, *, role: discord.Role):
        await ctx.channel.purge(limit=1)
        await member.add_roles(role)
        message = f'🥰 Role {role.mention} was given to {member.mention}.'
        channel = self.client.get_channel(753907336497725470)  # discord
        await channel.send(message)

    @commands.command(aliases=['removerole'])
    @commands.has_role(753889013257207839)  # admin
    async def remove_role(self, ctx, member: discord.Member, *, role: discord.Role):
        await ctx.channel.purge(limit=1)
        await member.remove_roles(role)
        message = f'😢 Role {role.mention} was removed from {member.mention}.'
        channel = self.client.get_channel(753907336497725470)  # discord
        await channel.send(message)


def setup(client):
    client.add_cog(AdminCommands(client))
