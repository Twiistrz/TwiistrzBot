# -----------------------------------------------------------
# (C) 2020 Emmanuel See Te, Cavite, Philippines
# -----------------------------------------------------------
import random
import json
from discord.ext import commands


class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def level(self, ctx):
        with open('levels.json', 'r') as file:
            users = json.load(file)
            if not ctx.author.bot:
                user = users[str(ctx.author.id)]
                lvl, exp = user['lvl'], round(user['exp'], 2)
                lvl = f'Max ({lvl})' if lvl >= 500 else lvl
                await ctx.send(f'Level: **{lvl}**\nExperience: **{exp}**')

    @commands.command()
    async def ping(self, ctx):
        """
        Ping command.

        :param ctx: Context
        """
        await ctx.send(f'Pong! - Time taken: **{round(self.client.latency * 1000)}ms**')

    @commands.command(name='8ball', aliases=['ask','8b'])
    async def _8ball(self, ctx, *, q):
        """
        8Ball command.

        :param ctx: Context
        :param q: Question
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
        8Ball custom error message.

        :param ctx: Context
        :param e: Error
        """
        if isinstance(e, commands.MissingRequiredArgument):
            await ctx.send('Please specify a question.')


def setup(client):
    client.add_cog(General(client))