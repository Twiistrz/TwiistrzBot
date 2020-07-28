# -----------------------------------------------------------
# (C) 2020 Emmanuel See Te, Cavite, Philippines
# -----------------------------------------------------------
"""
There comes a point in your bot’s development when you want to
organize a collection of commands, listeners, and some state into
one class. Cogs allow you to do just that.
"""
import random
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, client):
        """
        Initialize
        :param client:
        """
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        """
        Ping Command
        :param ctx: Context
        :return:
        """
        await ctx.send(f'Pong! - Time taken: **{round(self.client.latency * 1000)}ms**')

    @commands.command(aliases=['8ball', 'ask'])
    async def _8ball(self, ctx, *, q):
        """
        8Ball Command
        :param ctx: Context
        :param q: Question
        :return:
        """
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
        await ctx.send(f'**Q:** {q}\n**A:** {random.choice(responses)}')

    @_8ball.error
    async def _8ball_error(self, ctx, e):
        """
        8Ball Error
        :param ctx: Context
        :param e: Error
        :return:
        """
        if isinstance(e, commands.MissingRequiredArgument):
            await ctx.send('Please specify a question.')


def setup(client):
    client.add_cog(Test(client))
