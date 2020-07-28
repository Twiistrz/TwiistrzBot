# -----------------------------------------------------------
# (C) 2020 Emmanuel See Te, Cavite, Philippines
# -----------------------------------------------------------
import os
import json
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('prefixes.json', 'r') as file:
            prefixes = json.load(file)
        prefixes[str(guild.id)] = '.'
        with open('prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('prefixes.json', 'r') as file:
            prefixes = json.load(file)
        prefixes.pop(str(guild.id))
        with open('prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent=4)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Member join event

        :param member: Member
        """
        print(f'{member} has joined a server.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        Member remove or leave event.

        :param member: Member
        """
        print(f'{member} has left a server.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        """
        Command error listener.\n
        Errors: MissingRequiredArgument, CommandNotFound, MissingPermissions

        :param ctx: Context
        :param e: Error
        """
        if isinstance(e, (commands.CommandNotFound, commands.MissingRequiredArgument)):
            pass
        elif isinstance(e, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention}, {os.getenv("NO_PERMISSION")}')
        else:
            print(e)


def setup(client):
    client.add_cog(Events(client))
