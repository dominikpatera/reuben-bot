import os
from discord.ext import commands

client = commands.Bot(command_prefix='.')


@client.command()
@commands.has_role(754038174334058498)  # bot dev
async def load(ctx, extension):
    await ctx.channel.purge(limit=1)
    client.load_extension(f'cogs.{extension}')
    channel = client.get_channel(753971727431762000)  # status
    await channel.send(f'🔼 Extension "{extension}" was loaded.')


@client.command()
@commands.has_role(754038174334058498)  # bot dev
async def unload(ctx, extension):
    await ctx.channel.purge(limit=1)
    client.unload_extension(f'cogs.{extension}')
    channel = client.get_channel(753971727431762000)  # status
    await channel.send(f'🔽 Extension "{extension}" was unloaded.')


@client.command()
@commands.has_role(754038174334058498)  # bot dev
async def reload(ctx, extension=None):
    await ctx.channel.purge(limit=1)
    channel = client.get_channel(753971727431762000)  # status
    if extension is not None:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await channel.send(f'🔁 Extension "{extension}" was reloaded.')
    else:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                client.unload_extension(f'cogs.{filename[:-3]}')
                client.load_extension(f'cogs.{filename[:-3]}')
                await channel.send(f'🔁 Extension "{filename[:-3]}" was reloaded.')


@client.command()
@commands.has_role(754038174334058498)  # bot dev
async def shutdown(ctx):
    await ctx.channel.purge(limit=1)
    channel = client.get_channel(753971727431762000)  # status
    await channel.send('💤 I\'m going to sleep. Bye!')
    await ctx.bot.logout()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(os.environ["DISCORD_TOKEN"])
