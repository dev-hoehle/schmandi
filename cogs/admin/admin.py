from discord import app_commands
from datetime import datetime
import discord
from discord.ext import commands
from typing import Literal


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Ban someone")
    @discord.app_commands.describe(member="The member you want to ban")
    @discord.app_commands.describe(reason="Why do you want to ban this member?")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("You do not have the permission to ban members.", ephemeral=True)
            return

        if reason is None:
            reason = "No reason provided"

        # Send DM to member
        embed = discord.Embed(title=f"You have been banned from **{interaction.guild.name}**!", color=0x00D9FF,)
        embed.add_field(name="Banned by", value=interaction.user.mention)
        embed.add_field(name="Reason", value=reason)
        await member.send(embed=embed)
        await member.ban(reason=f"{reason} | Banned by: {interaction.user}")

        # Send message to channel
        embed = discord.Embed(title=" Member has been banned", color=0x00D9FF)
        embed.add_field(name="Banned User", value=member.mention)
        embed.add_field(name="Banned by", value=interaction.user.mention)
        embed.add_field(name="Reason", value=reason)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="kick", description="Kick someone")
    @discord.app_commands.describe(member="The member you want to kick")
    @discord.app_commands.describe(reason="Why do you want to kick this member?")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("You do not have the permission to kick members.", ephemeral=True)
            return

        if reason is None:
            reason = "No reason provided"

        # Send DM to member
        embed = discord.Embed(title=f"You have been kicked from **{interaction.guild.name}**!", color=0x00D9FF,)
        embed.add_field(name="Kicked by", value=interaction.user.mention)
        embed.add_field(name="Reason", value=reason)
        await member.send(embed=embed)
        await member.kick(reason=f"{reason} | Kicked by: {interaction.user}")


    @app_commands.command(name="lock_or_unlock", description="Locks or unlocks a channel")
    @discord.app_commands.describe(channel="The channel you want to lock or unlock")
    @discord.app_commands.describe(action="'lock' or 'unlock'")
    async def lock_or_unlock(self, interaction: discord.Interaction, channel: discord.TextChannel = None, action: Literal["lock", "unlock"] = "lock",):
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("You do not have the permission to lock or unlock channels.", ephemeral=True)
            return

        channel = channel or interaction.channel
        default_role = interaction.guild.default_role
        overwrite = discord.PermissionOverwrite(send_messages=None) if action=="unlock" else discord.PermissionOverwrite(send_messages=False)
        await channel.set_permissions(default_role, overwrite=overwrite)
        lockembed = discord.Embed(title=f"{action} channel", color=discord.Color.green(), timestamp=datetime.now())
        lockembed.add_field(name=f"The following channel has been {action}:", value=f"<#{channel.id}>")
        await interaction.response.send_message(embed=lockembed)


    @app_commands.command(name="nuke", description="Clears a whole channel")
    @discord.app_commands.describe(channel="The channel you want to nuke")
    async def nuke(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        if interaction.user.guild_permissions.manage_channels:
            channel = channel or interaction.channel
            try:
                new = await channel.clone(reason="Has been Nuked!")
                await channel.delete()
                await new.send("THIS CHANNEL HAS BEEN NUKED!")
            except discord.HTTPException:
                await interaction.response.send_message(f"An error occurred while nuking the channel {channel.name}.", ephemeral=True)
        else:
            nukeembed = discord.Embed(title="Error", color=discord.Color.dark_red())
            nukeembed.add_field(
                name="Permission Error",
                value=f"{interaction.user.mention} you don't have enough permissions to do that."
            )
            await interaction.response.send_message(embed=nukeembed)


    # Original from https://github.com/Ghostboy00/
    @app_commands.command(name="fakemessage", description="Fake a message from another member")
    @discord.app_commands.describe(member="The member you want to impersonate in the message.")
    @discord.app_commands.describe(message="The text you want to say")
    async def fakemessage(self, interaction: discord.Interaction, member: discord.Member, message: str):
        if interaction.user.guild_permissions.administrator:
            webhook_name = member.display_name
            webhook = await interaction.channel.create_webhook(name=webhook_name)
            try:
                await webhook.send(content=message, username=member.display_name, avatar_url=member.avatar)
                await interaction.response.send_message(f"Successfully sent fake message for {member.mention}", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"Failed to send fake message: {e}", ephemeral=True)
            finally:
                await webhook.delete()
        else:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)



async def setup(bot):
    await bot.add_cog(Admin(bot))
