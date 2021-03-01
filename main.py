# secret
token = "ODA2Mzk4OTI2MTE0MTI3OTMy.YBo3hg.decVJSwgLzPGHlCkPPjL8V7kRRA"

# ^ secret (token)

# Discord bot. copyright acutewoofTM jk nvm

# imports
import time

import discord
from discord.ext import commands
from pretty_help import PrettyHelp


class Moderation(
    commands.Cog, description="Commands for Moderation. Uses '$' as prefix"
):

    # unban command
    @commands.has_permissions(ban_members=True)
    @commands.command(name="unban", description="Unban a user")
    async def unban(self, ctx, user_id: int):
        user = await bot.fetch_user(user_id)
        unban_msg = discord.Embed(title=f"Unbanned {user}")

        await ctx.guild.unban(user)
        await ctx.channel.send(embed=unban_msg)

    # ban command
    @commands.has_permissions(ban_members=True)
    @commands.command(name="ban", help="Bans a user from the server.")
    async def ban(self, ctx, user: discord.Member, *, reason="No reason was provided"):
        ban_dm = discord.Embed(
            title="You have Been Banned! :expressionless:",
            description=f"**You have been banned from {ctx.message.guild.name}!**\n \n **Reason:`{reason}`**\n \n Please refrain from this kind of behavior in the future.",
        )

        ban_msg = discord.Embed(
            title=f"Banned {user}!",
            description=f"Reason: {reason}\nBy: {ctx.author.mention}",
        )

        await user.send(embed=ban_dm)
        await user.ban(reason=reason)
        await ctx.channel.send(embed=ban_msg)

    # kick command
    @commands.has_permissions(kick_members=True)
    @commands.command(name="kick", help="Kicks a user from the server.")
    async def kick(self, ctx, user: discord.Member, *, reason="No reason was provided"):
        kick_dm = discord.Embed(
            title="You have Been Kicked! :door:",
            description=f"**You have been kicked from {ctx.message.guild.name}!**\n \n **Reason:`{reason}`**\n \n Please refrain from this kind of behavior in the future.",
        )

        kick_msg = discord.Embed(
            title=f"Kicked {user}!",
            description=f"Reason: {reason}\nBy: {ctx.author.mention}",
        )

        await user.send(embed=kick_dm)
        await user.kick(reason=reason)
        await ctx.channel.send(embed=kick_msg)

    # unmute command
    @commands.has_permissions(manage_roles=True)
    @commands.command(
        name="unmute",
        help="Enables a user's permission to send messages in a text channel",
    )
    async def unmute(self, ctx, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await user.remove_roles(role)
        await ctx.channel.send(
            embed=discord.Embed(title=f"{ctx.author.mention} Unmuted {user}!")
        )

    # mute command
    @commands.has_permissions(manage_roles=True)
    @commands.command(
        name="mute",
        help="Disables a user's permission to send messages in a text channel. Time has to be entered in seconds",
    )
    async def mute(
        self, ctx, user: discord.Member, *, reason="No reason was provided", time=0
    ):
        if time > 0:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            await user.add_roles(role)
            muted_msg = discord.Embed(
                title=f"Muted {user}!",
                description=f"Reason: `{reason}`\nTime(in seconds): `{time}`\nBy: `{ctx.author.mention}`",
            )
            ctx.channel.send(embed=muted_msg)
            time.sleep(time)
            await user.remove_roles(role)
            await ctx.channel.send(embed=discord.Embed(title=f"Unmuted {user}!"))

        elif time == 0:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            await user.add_roles(role)
            muted_msg = discord.Embed(
                title=f"Muted {user}!",
                description=f"Reason: `{reason}`\nTime(in seconds): `{time}`\nBy: {ctx.author.mention}",
            )
            await ctx.channel.send(embed=muted_msg)

    # purge command
    @commands.has_permissions(manage_messages=True)
    @commands.command(name="purge", help="Bulk delete a set of messages")
    async def purge(self, ctx, limit=5):
        embed = discord.Embed(title=f"Deleted {limit} messages").set_author(
            name=ctx.author.display_name
        )
        await ctx.channel.purge(limit=limit + 1)
        msg = await ctx.channel.send(embed=embed)
        time.sleep(5)
        await msg.delete()


bot = commands.Bot(command_prefix="$", help_command=PrettyHelp())


@bot.event
async def on_ready():
    activity = discord.Activity(
        type=discord.ActivityType.watching, name="The Playground Discord"
    )
    await bot.change_presence(activity=activity)
    print("Bot Ready!")


@bot.event
async def on_message(message):
    print(f"{message.author}: {message.content}")
    await bot.process_commands(message)


bot.add_cog(Moderation())
bot.run(token)
