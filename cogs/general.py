# -----------------------------------------------------------
# (C) 2020 Emmanuel See Te, Cavite, Philippines
# -----------------------------------------------------------
import discord
import random
import json
import os
import time
from discord.ext import commands

lvl_xp = [5 * (i ** 2) + 50 * i + 100 for i in range(200)]


async def is_level_data(users, user):
    """
    Initialize levels data

    :param users: A list of members
    :param user: Author
    """
    if not str(user.id) in users:
        users[str(user.id)] = {}
        users[str(user.id)]['reputation'] = 0
        users[str(user.id)]['money'] = 0
        users[str(user.id)]['health'] = 120
        users[str(user.id)]['max-health'] = 120
        users[str(user.id)]['mana'] = 100
        users[str(user.id)]['max-mana'] = 100
        users[str(user.id)]['exp'] = 0
        users[str(user.id)]['lvl'] = 0
        users[str(user.id)]['timestamp'] = 0
        users[str(user.id)]['daily-timestamp'] = 0
        users[str(user.id)]['rep-timestamp'] = 0


def progress_bar(percent):
    bars = ''
    for i in range(0, int(percent)):
        bars += '▰'
    for j in range(0, 8 - int(percent)):
        bars += '▱'
    return bars


class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['rep'])
    async def reputation(self, ctx, member: discord.Member = None):
        """
        Give rep or receive rep!

        :param ctx: Context
        :param member: Member
        """
        with open('users.json', 'r') as f1:
            users = json.load(f1)
            if time.time() - users[str(ctx.author.id)]['rep-timestamp'] > 43200 and member:
                users[str(member.id)]['reputation'] += 1
                users[str(ctx.author.id)]['rep-timestamp'] = time.time()
                await ctx.send(f':up:  |  **{ctx.author.display_name} has given {member.mention} a reputation point!**')
                with open('users.json', 'w') as f2:
                    json.dump(users, f2, indent=4)
            else:
                if users[str(ctx.author.id)]['rep-timestamp'] > 0:
                    rep_countdown = time.gmtime(43200 - (time.time() - users[str(ctx.author.id)]['rep-timestamp']))
                    h, m, s = time.strftime('%H', rep_countdown), time.strftime('%M', rep_countdown), time.strftime('%S', rep_countdown)
                    await ctx.send(f':up:  |  **You can award more reputation in {h} hours, {m} minutes and {s} seconds.**')
                else:
                    await ctx.send(f':up:  |  **You can award more reputation point.**')

    @commands.command()
    async def daily(self, ctx):
        """
        Daily rewards.

        :param ctx: Context
        """
        with open('users.json', 'r') as f1:
            users = json.load(f1)
            if time.time() - users[str(ctx.author.id)]['daily-timestamp'] > 86400:
                users[str(ctx.author.id)]['money'] += 300
                users[str(ctx.author.id)]['daily-timestamp'] = time.time()
                await ctx.send(f'**{ctx.author.display_name}, you received your :dollar: 300 daily credits!**')
                with open('users.json', 'w') as f2:
                    json.dump(users, f2, indent=4)
            else:
                daily_countdown = time.gmtime(86400 - (time.time() - users[str(ctx.author.id)]['daily-timestamp']))
                h, m, s = time.strftime('%H', daily_countdown), time.strftime('%M', daily_countdown), time.strftime('%S', daily_countdown)
                await ctx.send(f':dollar:  |  **Daily credits reset in {h} hours, {m} minutes and {s} seconds.**')

    @commands.command(aliases=['lvl', 'lv'])
    async def profile(self, ctx, member: discord.Member = None):
        """
        A simple profile system

        :param ctx: Context
        :param member: Member
        """
        user = ctx.author if not member else member
        with open('users.json', 'r') as file:
            users = json.load(file)
            if not ctx.author.bot and not user.bot:
                await is_level_data(users, user)
                u = users[str(user.id)]
                lvl, exp = u['lvl'], int(u['exp'])
                hp, max_hp = u['health'], u['max-health']
                mp, max_mp = u['mana'], u['max-mana']
                lvl = f'Max ({lvl})' if lvl >= 100 else lvl
                embed = discord.Embed(
                    title=f'[Lv. {lvl}] {user.display_name}\'s Info',
                    color=discord.Color(value=int(os.getenv('COLOR_DEFAULT'), 16))
                )
                embed.set_thumbnail(url=user.avatar_url)
                embed.add_field(name=f'HP [{hp}/{max_hp}]', value=progress_bar((hp / max_hp) * 8), inline=True)
                embed.add_field(name=f'MP [{mp}/{max_mp}]', value=progress_bar((mp / max_mp) * 8), inline=True)
                embed.add_field(name=f'XP [{exp}/{lvl_xp[lvl]}]', value=progress_bar((exp / lvl_xp[lvl]) * 8), inline=True)
                embed.add_field(name='Credits', value=f'$ {int(u["money"])}', inline=True)
                embed.add_field(name='Reputations', value=f'+{int(u["reputation"])}rep', inline=True)
                embed.set_footer(text=f'ID: {user.id} ')
                await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """
        Ping command.

        :param ctx: Context
        """
        before = time.monotonic()
        ping = (time.monotonic() - before) * 1000
        print()
        await ctx.send(f':ping_pong:  |  **Pong! - {round(self.client.latency * 1000)}ms**')

    @commands.command(name='8ball', aliases=['ask', '8b'])
    async def _8ball(self, ctx, *, q):
        """
        8Ball command.

        :param ctx: Context
        :param q: Question
        """
        responses = ['It is certain.',
                     'It is decidedly so.',
                     'Without a doubt.',
                     'Yes - definitely.',
                     'You may rely on it.',
                     'As I see it, yes.',
                     'Most likely.',
                     'Outlook good.',
                     'Yes.',
                     'Signs point to yes.',
                     'Reply hazy, try again.',
                     'Ask again later.',
                     'Better not tell you now.',
                     'Cannot predict now.',
                     'Concentrate and ask again.',
                     'Don\'t count on it.',
                     'My reply is no.',
                     'My sources say no.',
                     'Outlook not so good.',
                     'Very doubtful.']
        await ctx.send(f':speech_balloon:  |  **{random.choice(responses)}**')

    @profile.error
    async def profile_error(self, ctx, error):
        """
        Profile custom error message.

        :param ctx: Context
        :param error: Error
        """
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(
                description='Member not found.',
                color=discord.Color(value=int(os.getenv('COLOR_ERROR'), 16))
            )
            await ctx.send(embed=embed)

    @_8ball.error
    async def _8ball_error(self, ctx, e):
        """
        8Ball custom error message.

        :param ctx: Context
        :param e: Error
        """
        if isinstance(e, commands.MissingRequiredArgument):
            await ctx.send(':warning:  |  **Please specify a question.**')


def setup(client):
    client.add_cog(General(client))
