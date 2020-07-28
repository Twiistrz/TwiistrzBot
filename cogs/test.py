# -----------------------------------------------------------
# (C) 2020 Emmanuel See Te, Cavite, Philippines
# -----------------------------------------------------------
"""
# There comes a point in your bot’s development when you want to
# organize a collection of commands, listeners, and some state into
# one class. Cogs allow you to do just that.
"""
import discord
import os
import random
import typing
from discord.ext import commands
from dotenv import load_dotenv

no_permission = 'Sorry you don\'t have permission to use this command.'


class Test(commands.Cog):
    # initialize the command
    def __init__(self, client):
        self.client = client

    # events
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print(f'Logged in as {self.client.user}')

    # commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! - Time taken: **{round(self.client.latency * 1000)}ms**')

    @commands.command()
    async def cogs(self, ctx):
        cogs = ''
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                cogs += filename[:-3] + ' '
        await ctx.send(f'Cogs: {cogs}')

    # kick command
    @commands.command()
    async def kick(self, ctx, member: discord.Member = None, *, reason=None):
        if ctx.author.id != os.getenv('DEV_ID'):
            await ctx.send(no_permission)
            return
        if member:
            await member.kick(reason=reason)
            if reason:
                await ctx.send(f'{ctx.author.name} kicked {member.mention} for {reason}')
            else:
                await ctx.send(f'{ctx.author.name} kicked {member.mention}')
            return
        await ctx.send('Usage: tw!kick [User]')

    # ban command
    @commands.command()
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if ctx.author.id != os.getenv('DEV_ID'):
            await ctx.send(no_permission)
            return
        if member:
            await member.ban(reason=reason)
            if reason:
                await ctx.send(f'{ctx.author.name} banned {member.mention} for {reason}')
            else:
                await ctx.send(f'{ctx.author.name} banned {member.mention}')
            return
        await ctx.send('Usage: tw!ban [User]')

    # unban command
    @commands.command()
    async def unban(self, ctx, *, member=None):
        if ctx.author.id != os.getenv('DEV_ID'):
            await ctx.send(no_permission)
            return
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{ctx.author.name} unbanned {user.mention}')
                return

    # clear command
    @commands.command()
    async def clear(self, ctx, *, amount: typing.Union[int, float, str]):
        if ctx.author.id != os.getenv('DEV_ID'):
            await ctx.send(no_permission)
            return
        if isinstance(amount, int) and amount > 0:
            if amount < 26:
                await ctx.message.delete()
                await ctx.channel.purge(limit=amount)
                await ctx.send(f'{ctx.author.mention} purged {amount} message(s)')
            else:
                await ctx.send('You can only purged up to 25 messages per request.')
        else:
            await ctx.send('Only numeric values.')

    # 8ball command
    @commands.command(aliases=['8ball', 'ask'])
    async def _8ball(self, ctx, *, question=None):
        responses = ['It is certain',
                     'It is decidedly so',
                     'Without a doubt',
                     'Yes - definitely',
                     'You may rely on it',
                     'As I see it, yes',
                     'Most likely',
                     'Outlook good',
                     'Yes',
                     'Signs point to yes',
                     'Reply hazy, try again',
                     'Ask again later',
                     'Better not tell you now',
                     'Cannot predict now',
                     'Concentrate and ask again',
                     'Don\'t count on it',
                     'My reply is no',
                     'My sources say no',
                     'Outlook not so good',
                     'Very doubtful']
        if not question:
            await ctx.send('Question must not be empty!')
            return
        await ctx.send(f'**Q:** {question}\n**A:** {random.choice(responses)}')

    # clear error
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify an amount of messages to delete.')


def setup(client):
    client.add_cog(Test(client))
