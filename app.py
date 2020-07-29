# -----------------------------------------------------------
# (C) 2020 Emmanuel See Te, Cavite, Philippines
# -----------------------------------------------------------
"""
Discord Python Docs: https://discordpy.readthedocs.io/en/latest/
Repository: https://github.com/Twiistrz/TwiistrzBot
"""
import os, discord, json, time
from itertools import cycle
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
status = cycle([
    '魔王学院の不適合者',
    '炎炎ノ消防隊',
    'ソードアート・オンライン',
    '宇崎ちゃんは遊びたい！',
    'とある科学の超電磁砲',
    'The God of High School'
])


async def get_prefix(client, message):
    """
    Get prefix of the current server.

    :param client:
    :param message: Message
    """
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix)


async def is_dev(ctx):
    """
    Check if the author is the developer of bot.

    :param ctx: Context
    :return: Boolean
    """
    return ctx.author.id == int(os.getenv('DEV_ID'))


async def update_data(users, user):
    """
    Initialize levels data

    :param users: A list of members
    :param user: Author
    """
    if not str(user.id) in users:
        users[str(user.id)] = {}
        users[str(user.id)]['exp'] = 0
        users[str(user.id)]['lvl'] = 1
        users[str(user.id)]['timestamp'] = 0


async def exp_up(users, user, exp):
    """
    Add Experience

    :param users: A list of members
    :param user: Author
    :param exp: Experience gain
    """
    if time.time() - users[str(user.id)]['timestamp'] > 30:
        users[str(user.id)]['exp'] += exp
        users[str(user.id)]['timestamp'] = time.time()


async def lvl_up(users, user, channel):
    """
    Level up

    :param users: A list of members
    :param user: Author
    :param channel: Channel
    """
    exp = users[str(user.id)]['exp']
    lvl_old = users[str(user.id)]['lvl']
    lvl_new = int(exp ** (1 / 4))
    if lvl_old < lvl_new:
        if lvl_new <= 100:
            await channel.send(f':tada: AYOOOOO {user.mention}, you just advanced to level {lvl_new}!')
            users[str(user.id)]['exp'] = users[str(user.id)]['exp'] / 16
            users[str(user.id)]['lvl'] = lvl_new


@client.event
async def on_ready():
    """
    When the bot is ready load all extensions that are available in 'cogs' directory.
    """
    cogs_loaded_count = 0
    cogs_loaded_name = ''
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cogs_loaded_count += 1
            cogs_loaded_name += filename[:-3] + ' '
            client.load_extension(f'cogs.{filename[:-3]}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="魔王学院の不適合者"))
    change_status.start()
    print(f'Logged in as {client.user}')
    print(f'Cogs Loaded ({cogs_loaded_count}): {cogs_loaded_name}')


@client.event
async def on_message(message):
    """
    Level up system
    """
    with open('levels.json', 'r') as f1:
        users = json.load(f1)
        if not message.author.bot:
            await update_data(users, message.author)
            exp = 0.1 * users[str(message.author.id)]['lvl'] ** 1.2 + (users[str(message.author.id)]['exp'] / 16)
            await exp_up(users, message.author, exp)
            await lvl_up(users, message.author, message.channel)
        with open('levels.json', 'w') as f2:
            json.dump(users, f2, indent=4)
    await client.process_commands(message)


@client.command()
@commands.check(is_dev)
async def load(ctx, ext=None):
    """
    Load extension command.

    :param ctx: Context
    :param ext: Extension
    """
    try:
        if ext:
            client.load_extension(f'cogs.{ext}')
            await ctx.send(f'Loaded {ext} cogs!')
        else:
            await ctx.send('Extension must not be empty!')
    except:
        await ctx.send(f'Unable to load {ext} cogs.')


@client.command()
@commands.check(is_dev)
async def unload(ctx, ext=None):
    """
    Unload extension command.

    :param ctx: Context
    :param ext: Extension
    """
    try:
        if ext:
            client.unload_extension(f'cogs.{ext}')
            await ctx.send(f'Unloaded {ext} cogs!')
        else:
            await ctx.send('Extension must not be empty!')
    except:
        await ctx.send(f'Unable to unload {ext} cogs.')


@client.command()
@commands.check(is_dev)
async def reload(ctx, ext=None):
    """
    Reload extension command.

    :param ctx: Context
    :param ext: Extension
    """
    try:
        if ext:
            client.unload_extension(f'cogs.{ext}')
            client.load_extension(f'cogs.{ext}')
            await ctx.send(f'Reloaded {ext} cogs!')
        else:
            await ctx.send(f'Extension must not be empty!')
    except:
        await ctx.send(f'Unable to reload {ext} cogs, make sure its loaded first!')


@tasks.loop(seconds=5)
async def change_status():
    """
    Change bot status every 5 seconds interval
    """
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

client.run(os.getenv('DISCORD_TOKEN'))
