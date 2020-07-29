# -----------------------------------------------------------
# (C) 2020 Emmanuel See Te, Cavite, Philippines
# -----------------------------------------------------------
"""
There comes a point in your bot’s development when you want to
organize a collection of commands, listeners, and some state into
one class. Cogs allow you to do just that.
"""
from discord.ext import commands
from discord.utils import get


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
