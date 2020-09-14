from discord.ext import commands
from classes.channels import Channels


class Status(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.channels = Channels().getChannels()

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        # await self.client.change_presence(status=discord.Status.idle, activity=discord.Game('I\'m emerging.'))
        print('Bot is online.')
        channel = self.client.get_channel(
            self.channels['bot']['status'])  # status
        await channel.send('👋 Hi, I\'m up.')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(
            self.channels['firstSteps']['new-users'])  # new users
        rules = self.client.get_channel(self.channels['firstSteps']['rules'])
        welcome = self.client.get_channel(
            self.channels['firstSteps']['welcome'])
        pickrole = self.client.get_channel(
            self.channels['firstSteps']['pick-role'])

        await channel.send(f'👋 Ahoj {member.mention}, vítej ve chlívku!')
        await member.send(f'🐷 VÍTEJ NA PIGGSCORDU! 🐷\n\nJsem rád, že si se k nám přidal! ❤️\n\nNezapomeň si přečíst {rules.mention},' +
                          f' ověřit se ✅ ve {welcome.mention} a vybrat roli v {pickrole.mention} dle tvých zájmů 👍!\n\nReuben\n*oink*')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        message = f'💬 "{ctx.message.content}" by {ctx.message.author.mention} in {ctx.message.channel.mention}.\n\n❌ {error}'

        channel = self.client.get_channel(
            self.channels['bot']['errors'])  # errors
        await channel.send(message)


def setup(client):
    client.add_cog(Status(client))
