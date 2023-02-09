from datetime import datetime, timedelta
from typing import Literal, Optional, Union

import discord
from discord import app_commands
from discord.ext import commands


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
    @discord.app_commands.describe(visibility="Should the channel be visible or invisible?")
    async def lock_or_unlock(self, interaction: discord.Interaction, channel: discord.TextChannel = None, action: Literal["lock", "unlock"] = "lock", visibility: Literal["visible", "invisible"] = "visible"):
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("You do not have the permission to lock or unlock channels.", ephemeral=True)
            return

        channel = channel or interaction.channel
        default_role = interaction.guild.default_role
        current_overwrite = channel.overwrites_for(default_role)

        if action == "unlock" and current_overwrite.send_messages == False:
            overwrite = discord.PermissionOverwrite(send_messages=None)
        elif action == "lock" and current_overwrite.send_messages != False:
            overwrite = discord.PermissionOverwrite(send_messages=False)
        else:
            await interaction.response.send_message(f"The channel is already {'locked' if action=='lock' else 'unlocked'}.", ephemeral=True)
            return

        if visibility == "invisible":
            await channel.edit(sync_permissions=False)

        await channel.set_permissions(default_role, overwrite=overwrite)

        if visibility == "invisible":
            await channel.edit(sync_permissions=True)

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



    @app_commands.command(name="timeout", description="Timeout a Member.")
    @discord.app_commands.describe(member="Who do you want to timeout?")
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, *, time: Literal["15s", "30s", "1min", "5min", "15min", "30min", "1h"], reason: str = None):
        if interaction.user.guild_permissions.administrator:
            timemap = {
                "15s": 15,
                "30s": 30,
                "1min": 60,
                "5min": 300,
                "15min": 900,
                "30min": 1800,
                "1h": 3600,
            }
            if not reason:
                reason = "None"

            try:
                oldtime = time
                time = timemap[time] 
            except KeyError:
                embed = discord.Embed(title="Timeout failed", color=0xff0000)
                embed.add_field(name="Error", value="Invalid timeout duration specified.", inline=True)
                return await interaction.response.send_message(embed=embed, ephemeral=True)
            
            timeout_duration = timedelta(seconds=int(time))
            try:
                timeout_result = await member.timeout(timeout_duration)
            except Exception as e:
                embed = discord.Embed(title="Tiemout failed", color=0xff0000)
                embed.add_field(name="Error", value=f"{e}", inline=True)
                return await interaction.response.send_message(embed=embed, ephemeral=True)
            
            embed = discord.Embed(title="Timeout Successful", color=0x00D9FF)
            embed.add_field(name="User", value=member.mention, inline=True)
            embed.add_field(name="Duration", value=f"{oldtime}", inline=True)
            embed.add_field(name="Reason", value=f"{reason}", inline=True)
            await interaction.response.send_message(embed=embed)

        else:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)





async def setup(bot):
    await bot.add_cog(Admin(bot))
