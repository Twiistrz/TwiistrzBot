# -----------------------------------------------------------
# (C) 2020 Emmanuel See Te, Cavite, Philippines
# -----------------------------------------------------------
"""
# There comes a point in your bot’s development when you want to
# organize a collection of commands, listeners, and some state into
# one class. Cogs allow you to do just that.
"""
import random
from discord.ext import commands


class Test(commands.Cog):
    # initialize the command
    def __init__(self, client):
        self.client = client

    # ping command
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! - Time taken: **{round(self.client.latency * 1000)}ms**')

    # 8ball command
    @commands.command(aliases=['8ball', 'ask'])
    async def _8ball(self, ctx, *, question):
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
        await ctx.send(f'**Q:** {question}\n**A:** {random.choice(responses)}')

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify a question.')


def setup(client):
    client.add_cog(Test(client))
