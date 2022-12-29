from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
import asyncio


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Ban someone")
    @app_commands.describe(member="The member you want to ban")
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        *,
        reason: str = None,
    ):
        if interaction.user.guild_permissions.ban_members:
            if reason is not None:
                embed = discord.Embed(
                    title=f"You have been banned from **{interaction.guild.name}**!",
                    color=0x00D9FF,
                )
                embed.add_field(name="Banned by", value=interaction.user.mention)
                embed.add_field(name="Reason", value=reason)
                await member.send(embed=embed)
                await member.ban(reason=reason + f" | Banned by: {interaction.user}")
                await member.ban(reason=f"Banned by: {interaction.user}")
                embed = discord.Embed(title=" Member has been banned", color=0x00D9FF)
                embed.add_field(name="Banned User", value=member.mention)
                embed.add_field(name="Banned by", value=interaction.user.mention)
                embed.add_field(name="Reason", value=reason)
                await interaction.response.send_message(embed=embed)

            else:
                embed = discord.Embed(
                    title=f"You have been banned from **{interaction.guild.name}**!",
                    color=0x00D9FF,
                )
                embed.add_field(name="Banned by", value=interaction.user.mention)
                embed.add_field(name="Reason", value="None")
                await member.send(embed=embed)
                await member.ban(reason=f"Banned by: {interaction.user}")
                embed = discord.Embed(title=" Member has been banned", color=0x00D9FF)
                embed.add_field(name="Banned User", value=member.mention)
                embed.add_field(name="Banned by", value=interaction.user.mention)
                embed.add_field(name="Reason", value="None")
                await interaction.response.send_message(embed=embed)
        else:
            banembed = discord.Embed(
                title="Error", color=discord.Color.dark_red(), timestamp=datetime.now()
            )

            banembed.add_field(
                name="Something wrent wrong",
                value=f"<@{interaction.user.id}> you don`t have enough permissions to do that.",
            )

            await interaction.response.send_message(embed=banembed, ephemeral=True)
            banembed.clear_fields()

    @app_commands.command(name="kick", description="Kick someone")
    @app_commands.describe(member="The member you want to kick")
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        *,
        reason: str = None,
    ):
        if interaction.user.guild_permissions.kick_members:
            if reason is not None:
                embed = discord.Embed(
                    title=f"You have been kicked from **{interaction.guild.name}**!",
                    color=0x00D9FF,
                )
                embed.add_field(name="Kicked by", value=interaction.user.mention)
                embed.add_field(name="Reason", value=reason)
                await member.send(embed=embed)
                await member.kick(reason=reason + f" | Kicked by: {interaction.user}")
                await member.kick(reason=f"Kicked by: {interaction.user}")
                embed = discord.Embed(title=" Member has been kicked", color=0x00D9FF)
                embed.add_field(name="Kicked User", value=interaction.user.mention)
                embed.add_field(name="Kicked by", value=member.mention)
                embed.add_field(name="Reason", value=reason)
                await interaction.response.send_message(embed=embed)

            else:
                embed = discord.Embed(
                    title=f"You have been kicked from **{interaction.guild.name}**!",
                    color=0x00D9FF,
                )
                embed.add_field(name="Kicked by", value=interaction.user.mention)
                embed.add_field(name="Reason", value="None")
                await member.send(embed=embed)
                await member.kick(reason=f"Kicked by: {interaction.user}")
                embed = discord.Embed(title=" Member has been kicked", color=0x00D9FF)
                embed.add_field(name="Kicked User", value=member.mention)
                embed.add_field(name="Kicked by", value=interaction.user.mention)
                embed.add_field(name="Reason", value="None")
                await interaction.response.send_message(embed=embed)
        else:
            kickembed = discord.Embed(
                title="Error", color=discord.Color.dark_red(), timestamp=datetime.now()
            )

            kickembed.add_field(
                name="Something wrent wrong",
                value=f"<@{interaction.user.id}> you don`t have enough permissions to do that.",
            )

            await interaction.response.send_message(embed=kickembed, ephemeral=True)
            kickembed.clear_fields()

    @app_commands.command(name="lock", description="Locks a channel channel")
    @app_commands.describe(channel="The channel you want to lock")
    async def lock(
        self, interaction: discord.Interaction, channel: discord.TextChannel = None
    ):
        if interaction.user.guild_permissions.manage_channels:
            channel = channel or interaction.channel
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(
                interaction.guild.default_role, overwrite=overwrite
            )

            lockembed = discord.Embed(
                title="Locked channel",
                color=discord.Color.green(),
                timestamp=datetime.now(),
            )

            lockembed.add_field(
                name=f"The following channel has been locked:",
                value=f"<#{channel.id}>",
            )
            await interaction.response.send_message(embed=lockembed)
        else:
            lockembed = discord.Embed(
                title="Error", color=discord.Color.dark_red(), timestamp=datetime.now()
            )

            lockembed.add_field(
                name="Something wrent wrong",
                value=f"<@{interaction.user.id}> you don`t have enough permissions to do that.",
            )

            await interaction.response.send_message(embed=lockembed, ephemeral=True)
            lockembed.clear_fields()

    @app_commands.command(name="unlock", description="Unlocks a channel")
    @app_commands.describe(channel="The channel you want to unlock")
    async def unlock(
        self, interaction: discord.Interaction, channel: discord.TextChannel = None
    ):
        if interaction.user.guild_permissions.manage_channels:
            channel = channel or interaction.channel
            overwrite = channel.overwrites_for(interaction.guild.default_role)
            overwrite.send_messages = True
            await channel.set_permissions(
                interaction.guild.default_role, overwrite=overwrite
            )

            lockembed = discord.Embed(
                title="Unlocked channel",
                color=discord.Color.green(),
                timestamp=datetime.now(),
            )

            lockembed.add_field(
                name=f"The following channel has been unlocked:",
                value=f"<#{channel.id}>",
            )
            await interaction.response.send_message(embed=lockembed)
        else:
            lockembed = discord.Embed(
                title="Error", color=discord.Color.dark_red(), timestamp=datetime.now()
            )

            lockembed.add_field(
                name="Something wrent wrong",
                value=f"<@{interaction.user.id}> you don`t have enough permissions to do that.",
            )

            await interaction.response.send_message(embed=lockembed, ephemeral=True)
            lockembed.clear_fields()

    @app_commands.command(name="nuke", description="Clears a whole channel")
    @app_commands.describe(channel="The channel you want to nuke")
    async def nuke(
        self, interaction: discord.Interaction, channel: discord.TextChannel = None
    ):
        if interaction.user.guild_permissions.manage_channels:
            if channel is None:
                channel = interaction.channel
            nuke_channel = discord.utils.get(
                interaction.guild.channels, name=channel.name
            )

            if nuke_channel is not None:
                new_channel = await nuke_channel.clone(reason="Has been Nuked!")
                await nuke_channel.delete()
                await new_channel.send("THIS CHANNEL HAS BEEN NUKED!")

            else:
                await interaction.response.send_message(
                    f"No channel named {channel.name} was found!", ephemeral=True
                )
        else:
            nukeembed = discord.Embed(
                title="Error", color=discord.Color.dark_red(), timestamp=datetime.now()
            )

            nukeembed.add_field(
                name="Something wrent wrong",
                value=f"<@{interaction.user.id}> you don`t have enough permissions to do that.",
            )

            await interaction.response.send_message(embed=nukeembed, ephemeral=True)
            nukeembed.clear_fields()

    # Original from https://github.com/Ghostboy00/
    @app_commands.command(
        name="fakemessage", description="Fake a message from another member"
    )
    @app_commands.describe(member="The member you want to say something")
    @app_commands.describe(message="The text you want a to say")
    async def fakemessage(
        self, interaction: discord.Interaction, member: discord.Member, message: str
    ):

        if interaction.user.guild_permissions.administrator:

            getwebhook = await interaction.channel.create_webhook(
                name=str(member.display_name)
            )

            await getwebhook.send(str(message), avatar_url=member.display_avatar.url)
            await getwebhook.delete()

            embed = discord.Embed(title="Webhook sent!", color=0x09F118)
            embed.add_field(
                name="Successfully sent message",
                value=f"Faked for <@{member.id}>",
                inline=False,
            )
            embed.add_field(name="Content", value=message, inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            embed.clear_fields()

        else:
            fakemessage = discord.Embed(
                title="Error", color=discord.Color.dark_red(), timestamp=datetime.now()
            )

            fakemessage.add_field(
                name="Something wrent wrong",
                value=f"<@{interaction.user.id}> you don`t have enough permissions to do that.",
            )

            await interaction.response.send_message(embed=fakemessage, ephemeral=True)
            fakemessage.clear_fields()


async def setup(bot):
    await bot.add_cog(admin(bot))
