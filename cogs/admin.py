# -----------------------------------------------------------
# (C) 2020 Emmanuel See Te, Cavite, Philippines
# -----------------------------------------------------------
import discord
import os
import random
import typing
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class Admin(commands.Cog):
    # initialize
    def __init__(self, client):
        self.client = client

    # cogs command
    @commands.command()
    async def cogs(self, ctx):
        if ctx.author.id != int(os.getenv('DEV_ID')):
            await ctx.send(os.getenv('NO_PERMISSION'))
            return
        cogs = ''
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                cogs += filename[:-3] + ' '
        await ctx.send(f'Cogs: {cogs}')

    # kick command
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.id != int(os.getenv('DEV_ID')):
            await ctx.send(os.getenv('NO_PERMISSION'))
            return
        await member.kick(reason=reason)
        if reason:
            await ctx.send(f'{ctx.author.name} kicked {member.mention} for {reason}')
        else:
            await ctx.send(f'{ctx.author.name} kicked {member.mention}')

    # ban command
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.id != int(os.getenv('DEV_ID')):
            await ctx.send(os.getenv('NO_PERMISSION'))
            return
        await member.ban(reason=reason)
        if reason:
            await ctx.send(f'{ctx.author.name} banned {member.mention} for {reason}')
        else:
            await ctx.send(f'{ctx.author.name} banned {member.mention}')

    # unban command
    @commands.command()
    async def unban(self, ctx, *, member=None):
        if ctx.author.id != int(os.getenv('DEV_ID')):
            await ctx.send(os.getenv('NO_PERMISSION'))
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
        if ctx.author.id != int(os.getenv('DEV_ID')):
            await ctx.send(os.getenv('NO_PERMISSION'))
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

    # kick error
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the name of member to kick.')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Member not found.')

    # ban error
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the name of member to ban.')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Member not found.')

    # clear error
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify an amount of messages to delete.')


def setup(client):
    client.add_cog(Admin(client))
