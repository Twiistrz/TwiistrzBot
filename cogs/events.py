# -----------------------------------------------------------
# (C) 2020 Emmanuel See Te, Cavite, Philippines
# -----------------------------------------------------------
from discord.ext import commands


class Events(commands.Cog):
    # initialize
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} has joined a server.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left a server.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Errors: MissingRequiredArgument, CommandNotFound
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Invalid command.')


def setup(client):
    client.add_cog(Events(client))
