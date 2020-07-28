# -----------------------------------------------------------
# (C) 2020 Emmanuel See Te, Cavite, Philippines
# -----------------------------------------------------------
import discord
import typing
import json
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, prefix):
        """
        Change prefix of the bot.

        :param ctx: Context
        :param prefix: New prefix of the bot
        """
        with open('prefixes.json', 'r') as file:
            prefixes = json.load(file)
        prefixes[str(ctx.guild.id)] = prefix
        with open('prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent=4)
        await ctx.send(f'Prefix set to `{prefix}`')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """
        Kick command.

        :param ctx: Context
        :param member: Member
        :param reason: Reason
        """
        await member.kick(reason=reason)
        if reason:
            await ctx.send(f'{ctx.author.name} kicked {member.mention} for {reason}')
        else:
            await ctx.send(f'{ctx.author.name} kicked {member.mention}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """
        Ban command.

        :param ctx: Context
        :param member: Member
        :param reason: Reason
        """
        await member.ban(reason=reason)
        if reason:
            await ctx.send(f'{ctx.author.name} banned {member.mention} for {reason}')
        else:
            await ctx.send(f'{ctx.author.name} banned {member.mention}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member=None):
        """
        Unban command.

        :param ctx: Context
        :param member: Member
        """
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{ctx.author.name} unbanned {user.mention}')
                return

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, *, amount: typing.Union[int, float, str]):
        """
        Clear messages command.

        :param ctx: Context
        :param amount: Amount of message to be deleted, maximum of 25.
        """
        if isinstance(amount, int) and amount > 0:
            if amount < 26:
                await ctx.message.delete()
                await ctx.channel.purge(limit=amount)
                await ctx.send(f'{ctx.author.mention} purged {amount} message(s)')
            else:
                await ctx.send('You can only purged up to 25 messages per request.')
        else:
            await ctx.send('Only numeric values.')

    @setprefix.error
    async def setprefix_error(self, ctx, e):
        """
        Set prefix custom error message.

        :param ctx: Context
        :param e: Error
        """
        if isinstance(e, commands.MissingRequiredArgument):
            await ctx.send('Please input a new prefix.')

    @kick.error
    async def kick_error(self, ctx, error):
        """
        Kick custom error message.

        :param ctx: Context
        :param error: Error
        """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the name of member to kick.')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Member not found.')

    @ban.error
    async def ban_error(self, ctx, error):
        """
        Ban custom error message.

        :param ctx: Context
        :param error: Error
        """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify the name of member to ban.')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Member not found.')

    @clear.error
    async def clear_error(self, ctx, error):
        """
        Clear custom error message.

        :param ctx: Context
        :param error: Error
        """
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify an amount of messages to delete.')


def setup(client):
    client.add_cog(Admin(client))
