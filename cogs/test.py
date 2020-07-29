# -----------------------------------------------------------
# (C) 2020 Emmanuel See Te, Cavite, Philippines
# -----------------------------------------------------------
"""
There comes a point in your bot’s development when you want to
organize a collection of commands, listeners, and some state into
one class. Cogs allow you to do just that.
"""
import json
import random
import time

from discord.ext import commands
from discord.utils import get

players = {}


async def update_data(users, user):
    if not str(user.id) in users:
        users[str(user.id)] = {}
        users[str(user.id)]['exp'] = 0
        users[str(user.id)]['lvl'] = 1
        users[str(user.id)]['timestamp'] = 0


async def exp_up(users, user, exp):
    # if time.time() - users[str(user.id)]['timestamp'] > 30:
    users[str(user.id)]['exp'] += exp
    users[str(user.id)]['timestamp'] = time.time()


async def lvl_up(users, user, channel):
    exp = users[str(user.id)]['exp']
    lvl_old = users[str(user.id)]['lvl']
    lvl_new = int(exp ** (1 / 4))
    print(f'{lvl_old} : {lvl_new}')
    if lvl_old < lvl_new:
        if lvl_new <= 100:
            await channel.send(f':tada: AYOOOOO {user.mention}, you just advanced to level {lvl_new}!')
            users[str(user.id)]['exp'] = users[str(user.id)]['exp'] / 16
            users[str(user.id)]['lvl'] = lvl_new


class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        with open('levels.json', 'r') as f1:
            users = json.load(f1)
            if not message.author.bot:
                await update_data(users, message.author)
                exp = 0.1 * users[str(message.author.id)]['lvl'] ** 1.2 + (users[str(message.author.id)]['exp'] / 16)
                print(f'{message.author.name}: {exp}')
                await exp_up(users, message.author, exp)
                await lvl_up(users, message.author, message.channel)
            with open('levels.json', 'w') as f2:
                json.dump(users, f2, indent=4)

    @commands.command()
    async def level(self, ctx):
        with open('levels.json', 'r') as f:
            users = json.load(f)
            if not ctx.author.bot:
                if users[str(ctx.author.id)]["lvl"] >= 100:
                    await ctx.send(f'Level: Max ({users[str(ctx.author.id)]["lvl"]})\nExperience: {users[str(ctx.author.id)]["exp"]}')
                else:
                    await ctx.send(f'Level: {users[str(ctx.author.id)]["lvl"]}\nExperience: {users[str(ctx.author.id)]["exp"]}')

    @commands.command()
    async def kofi(self, ctx):
        """
        My ko-fi support page.

        :param ctx: Context
        """
        await ctx.send('Ko-fi: https://ko-fi.com/twiistrz')

    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send('You are not connected to a voice channel.')
            return
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        try:
            voice = ctx.message.guild.voice_client
            await voice.disconnect()
        except:
            await ctx.send('Not in any voice channel.')

    # @commands.command()
    # async def play(self, ctx, url):
    #     print(url)
    #     channel = ctx.message.author.voice.channel
    #     if not channel:
    #         await ctx.send('You are not connected to a voice channel.')
    #         return
    #     voice = get(self.client.voice_clients, guild=ctx.guild)
    #     if voice and voice.is_connected():
    #         await voice.move_to(channel)
    #     else:
    #         voice = await channel.connect()
    #     async with ctx.typing():
    #         player = await YTDLSource.from_url(url, loop=self.client.loop)
    #         ctx.voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    #     await ctx.send('Now playing: {}'.format(player.title))


def setup(client):
    client.add_cog(Test(client))
