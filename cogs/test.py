# -----------------------------------------------------------
# (C) 2020 Emmanuel See Te, Cavite, Philippines
# -----------------------------------------------------------
"""
There comes a point in your bot’s development when you want to
organize a collection of commands, listeners, and some state into
one class. Cogs allow you to do just that.
"""
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kofi(self, ctx):
        """
        My ko-fi support page.

        :param ctx: Context
        """
        await ctx.send('Ko-fi: https://ko-fi.com/twiistrz')


def setup(client):
    client.add_cog(Test(client))
