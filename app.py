# -----------------------------------------------------------
# (C) 2020 Emmanuel See Te, Cavite, Philippines
# -----------------------------------------------------------
"""
Docs: https://discordpy.readthedocs.io/en/latest/
Repository: https://github.com/Twiistrz/TwiistrzBot
"""
import discord
import os
from discord.ext import commands, tasks
from itertools import cycle
from dotenv import load_dotenv

load_dotenv()
client = commands.Bot(command_prefix='.')
status = cycle([
    '魔王学院の不適合者',
    '炎炎ノ消防隊',
    'ソードアート・オンライン',
    '宇崎ちゃんは遊びたい！',
    'とある科学の超電磁砲',
    'The God of High School'
])


@client.event
async def on_ready():
    # load all cogs on startup
    cogs_loaded_count = 0
    cogs_loaded_name = ''
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cogs_loaded_count += 1
            cogs_loaded_name += filename[:-3] + ' '
            client.load_extension(f'cogs.{filename[:-3]}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Twiistrz Basement"))
    change_status.start()
    print(f'Logged in as {client.user}')
    print(f'Cogs Loaded ({cogs_loaded_count}): {cogs_loaded_name}')


# load command
@client.command()
async def load(ctx, extension=None):
    try:
        if extension:
            client.load_extension(f'cogs.{extension}')
            await ctx.send(f'Loaded {extension} cogs!')
        else:
            await ctx.send('Extension must not be empty!')
    except:
        await ctx.send(f'Unable to load {extension} cogs.')


# unload command
@client.command()
async def unload(ctx, extension=None):
    try:
        if extension:
            client.unload_extension(f'cogs.{extension}')
            await ctx.send(f'Unloaded {extension} cogs!')
        else:
            await ctx.send('Extension must not be empty!')
    except:
        await ctx.send(f'Unable to unload {extension} cogs.')


# reload command
@client.command()
async def reload(ctx, extension=None):
    try:
        if extension:
            client.unload_extension(f'cogs.{extension}')
            client.load_extension(f'cogs.{extension}')
            await ctx.send(f'Reloaded {extension} cogs!')
        else:
            await ctx.send(f'Extension must not be empty!')
    except:
        await ctx.send(f'Unable to reload {extension} cogs, make sure its loaded first!')


@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

client.run(os.getenv('DISCORD_TOKEN'))
