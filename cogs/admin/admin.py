import asyncio
import re
import sys
from datetime import datetime
from typing import Literal

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from helpers.general import print_failure_message
from helpers.util import check_bot_perms, check_channel, check_user_perms

sys.dont_write_bytecode = True

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Ban someone")
    @discord.app_commands.describe(member="The member you want to ban")
    @discord.app_commands.describe(reason="Why do you want to ban this member?")
    async def ban(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        try:
            bot_perms = await check_bot_perms(interaction, "ban_members")
            user_perms = await check_user_perms(interaction, "ban_members")
            if not bot_perms or not user_perms:
                return

            if reason is None:
                reason = "No reason provided"

            # Send a DM to the banned member
            try:
                embed = discord.Embed(
                    title=f"You have been banned from **{interaction.guild.name}**!",
                    color=0x00D9FF
                ).add_field(
                    name="Banned by",
                    value=interaction.user.mention
                ).add_field(
                    name="Reason",
                    value=reason
                )
                await member.send(embed=embed)
            except Exception as e:
                print_failure_message(f"Failed to DM {member}: {e}")


            embed = discord.Embed(
                title=" Member has been banned",
                color=0x00D9FF
            ).add_field(
                name="Banned User",
                value=member.mention
            ).add_field(
                name="Banned by",
                value=interaction.user.mention
            ).add_field(
                name="Reason",
                value=reason
            )
            await interaction.response.send_message(embed=embed)

            # Ban the member and provide the reason and the user who banned them
            try:
                await member.ban(reason=f"{reason} | Banned by: {interaction.user.name}")
            except Exception as e:
                print_failure_message(f"Failed to ban {member}: {e}")
        except Exception as e:
            print_failure_message(f"An error occurred while executing the ban command: {e}")

    @app_commands.command(name="softban", description="Basically a kick. But also deletes a useres message from the past week.")
    @discord.app_commands.describe(member="The member you want to softban")
    @discord.app_commands.describe(reason="Why do you want to softban this member?")
    async def softban(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        try:
            bot_perms = await check_bot_perms(interaction, "ban_members")
            user_perms = await check_user_perms(interaction, "ban_members")
            if not bot_perms or not user_perms:
                return

            if reason is None:
                reason = "No reason provided"

            try:
                embed = discord.Embed(
                    title=f"You have been softbanned from **{interaction.guild.name}**!",
                    color=0x00D9FF
                ).add_field(
                    name="Softbanned by",
                    value=interaction.user.mention
                ).add_field(
                    name="Reason",
                    value=reason
                )
                await member.send(embed=embed)
            except Exception as e:
                print_failure_message(f"Failed to DM {member}: {e}")


            try:                
                await member.ban(reason=f"{reason} | Softbanned by: {interaction.user.name}", delete_message_days=7)
            except Exception as e:
                print_failure_message(f"Failed to softban {member}: {e}")

           
            try:
                await interaction.guild.unban(member, reason="Softban lift")
            except Exception as e:
                print_failure_message(f"Failed to unban {member} after softban: {e}")

            embed = discord.Embed(
                title="Member has been softbanned",
                color=0x00D9FF
            ).add_field(
                name="Softbanned User",
                value=member.mention
            ).add_field(
                name="Softbanned by",
                value=interaction.user.mention
            ).add_field(
                name="Reason",
                value=reason
            )
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print_failure_message(f"An error occurred while executing the softban command: {e}")



    @app_commands.command(name="kick", description="Kick someone")
    @discord.app_commands.describe(member="The member you want to kick")
    @discord.app_commands.describe(reason="Why do you want to kick this member?")
    async def kick(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = None):
        try:
            bot_perms = await check_bot_perms(interaction, "kick_members")
            user_perms = await check_user_perms(interaction, "kick_members")
            if not bot_perms or not user_perms:
                return

            # Set a default reason if none is provided
            if reason is None:
                reason = "No reason provided"

            # Send a direct message to the kicked member
            embed = discord.Embed(
                title=f"You have been kicked from **{interaction.guild.name}**!",
                color=0x00D9FF
            ).add_field(
                name="Kicked by",
                value=interaction.user.mention
            ).add_field(
                name="Reason",
                value=reason
            )
            await member.send(embed=embed)

            # Kick the member and provide the reason
            await member.kick(reason=f"{reason} | Kicked by: {interaction.user.name}")

            # Send a success message to the user
            embed = discord.Embed(
                title="Member kicked",
                color=0x00D9FF
            ).add_field(
                name="Kicked User",
                value=member.mention
            ).add_field(
                name="Kicked by",
                value=interaction.user.mention
            ).add_field(
                name="Reason",
                value=reason
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except discord.Forbidden as e:
            embed = discord.Embed(
                title="Error",
                color=0xff0000
            ).add_field(
                name="Message",
                value=e.__str__(),
                inline=True
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            embed = discord.Embed(
                title="Error",
                color=0xff0000
            ).add_field(
                name="Message",
                value=e.__str__(),
                inline=True
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)





    @app_commands.command(name="toggle_channel_lock", description="Locks or unlocks a channel")
    @discord.app_commands.describe(channel="The channel you want to lock or unlock")
    @discord.app_commands.describe(action="'lock' or 'unlock'")
    @discord.app_commands.describe(visibility="'visible' or 'invisible'")
    async def toggle_channel_lock(self, interaction, channel: discord.TextChannel = None, action: Literal["lock", "unlock"] = "lock",
                            visibility: Literal["visible", "invisible"] = "visible"):

        bot_perms = await check_bot_perms(interaction, "manage_channels")
        user_perms = await check_user_perms(interaction, "manage_channels")
        if not bot_perms or not user_perms:
            return
            
        channelToUse = check_channel(interaction=interaction, channel=channel)

        # Get the permissions for the @everyone role for the channel
        default_role = interaction.guild.default_role
        current_overwrite = channelToUse.overwrites_for(default_role)

        # Determine the new permission overwrite for the @everyone role
        if action == "unlock" and current_overwrite.send_messages == False:
            overwrite = discord.PermissionOverwrite(send_messages=None, view_channel=None)
        elif action == "lock" and current_overwrite.send_messages != False:
            overwrite = discord.PermissionOverwrite(send_messages=False, view_channel=False)
        else:
            await interaction.response.send_message(f"The channel is already {'locked' if action=='lock' else 'unlocked'}.", ephemeral=True)
            return

        # Set the new permissions for the @everyone role
        try:
            await channelToUse.set_permissions(default_role, overwrite=overwrite)
        except discord.Forbidden:
            await interaction.response.send_message(
                f"I do not have the permission to manage permissions for <#{channelToUse.id}>.",
                ephemeral=True
            )
            return

        # If the channel is being made invisible, temporarily turn off permission syncing
        if visibility == "invisible":
            try:
                await channelToUse.edit(sync_permissions=False)
            except discord.Forbidden:
                await interaction.response.send_message(f"I do not have the permission to edit the channel <#{channelToUse.id}>.", ephemeral=True)
                return

        # If the channel is being made visible, turn permission syncing back on
        if visibility == "visible":
            try:
                await channelToUse.edit(sync_permissions=True)
            except discord.Forbidden:
                return await interaction.response.send_message(f"I do not have the permission to edit the channel <#{channelToUse.id}>.", ephemeral=True)

        # Update the lock/unlock status in the embed title
        action_title = "Locked" if action == "lock" else "Unlocked"

        lockembed = discord.Embed(
            title=f"{action_title} channel",
            color=discord.Color.green(),
            timestamp=datetime.now()
        ).add_field(
            name=f"The following channel has been {action}:",
            value=f"<#{channelToUse.id}>"
        )
        await interaction.response.send_message(embed=lockembed)




    @app_commands.command(name="nuke", description="Nuke a channel")
    @discord.app_commands.describe(channel="The channel you want to nuke")
    async def nuke(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        bot_perms = await check_bot_perms(interaction, "manage_channels")
        user_perms = await check_user_perms(interaction, "manage_channels")
        if not bot_perms or not user_perms:
            return

        check_channel(interaction, channel)
        try:
            await interaction.response.send_message("Channel will be nuked shortly.", ephemeral=True)

            # Clone the channel and move it to the original channel's position, then delete the original channel
            new = await channel.clone(reason="Has been Nuked!")
            await new.edit(position=channel.position)
            await channel.delete()

            # Send an embed in the new channel to indicate that the nuke was successful
            embed = discord.Embed(
                title="Nuke Successful",
                description=f"This channel has been nuked!",
                color=discord.Color.red()
            ).set_image(
                url="https://media.discordapp.net/attachments/811143476522909718/819507596302090261/boom.gif"
            ).set_footer(
                text=f"Requested by {interaction.user.name}",
                icon_url=interaction.user.avatar
            )
            await new.send(embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred while nuking the channel. Please try again later.",
                color=discord.Color.red()
            ).set_footer(
                text=f"Requested by {interaction.user.name}",
                icon_url=interaction.user.avatar
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @app_commands.command(name="fakemessage", description="Fake a message from another member")
    @discord.app_commands.describe(member="The member you want to impersonate in the message.")
    @discord.app_commands.describe(message="The text you want to say")
    @discord.app_commands.describe(channel="The channel where the fake message should be sent. (Optional)")
    async def fakemessage(self, interaction: discord.Interaction, member: discord.Member, message: str, channel: discord.TextChannel = None):

        bot_perms = await check_bot_perms(interaction, "manage_webhooks")
        user_perms = await check_user_perms(interaction, "manage_webhooks")
        if not bot_perms or not user_perms:
            return
            

        channelToUse = check_channel(interaction=interaction, channel=channel)

        webhook = None
        cloned_emojis = []

        try:
            # Create a webhook with the member's display name
            webhook_name = member.display_name
            webhook = await channelToUse.create_webhook(name=webhook_name)

            # Check for emojis in the message
            emojis = re.findall(r"<(a)?:\w+:(\d+)>", message)

            # Clone emojis to the server if they are not already present
            for animated, emoji_id in emojis:
                emoji = discord.utils.get(interaction.guild.emojis, id=int(emoji_id))
                if not emoji:
                    # Use the clone_emote logic to clone the emoji
                    emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{'gif' if animated else 'png'}"
                    async with aiohttp.ClientSession() as session:
                        get_bytes = await session.get(url=emoji_url)
                        if get_bytes.status != 200:
                            await interaction.response.send_message("Failed to clone emote: Invalid emote.", ephemeral=True)
                            return

                        emoji_bytes = bytes(await get_bytes.read())

                    emoji_name = f"fake_{emoji_id}"
                    emoji = await interaction.guild.create_custom_emoji(name=emoji_name, image=emoji_bytes)
                    cloned_emojis.append(emoji)

            # Modify the message to include the cloned emojis
            for emoji in cloned_emojis:
                message = re.sub(r"<(a)?:\w+:(\d+)>", str(emoji), message)

            # Send the fake message using the webhook
            await webhook.send(content=message, username=member.display_name, avatar_url=member.display_avatar)

            await interaction.response.send_message(f"Successfully sent fake message for {member.mention} in {channelToUse.mention}", ephemeral=True)

        except discord.errors.Forbidden:
            await interaction.response.send_message("I cannot create a webhook in this channel.", ephemeral=True)
        except discord.errors.HTTPException as e:
            await interaction.response.send_message(f"Failed to send fake message: {e}", ephemeral=True)
        finally:
            # Delete the webhook after the fake message is sent
            await asyncio.sleep(10)
            if webhook:
                await webhook.delete()
            for emoji in cloned_emojis:
                await emoji.delete()


    @app_commands.command(name="edit_message", description="Edit a message in the current or specified channel")
    @discord.app_commands.describe(
        channel="The channel where the message is located (optional, defaults to the current channel)",
        message_id="The ID of the message you want to edit",
        content="The new content for the message"
    )
    async def edit_message(self, interaction: discord.Interaction, channel: discord.TextChannel = None, message_id: str = None, content: str = None):
        channelToUse = check_channel(interaction=interaction, channel=channel)

        if message_id is None:
            return await interaction.response.send_message("Please provide the ID of the message you want to edit.", ephemeral=True)

        try:
            # Fetch the message using the provided message ID
            message = await channelToUse.fetch_message(message_id)
        except discord.NotFound:
            return await interaction.response.send_message("The specified message was not found.", ephemeral=True)


        bot_perms = await check_bot_perms(interaction, "manage_messages")
        user_perms = await check_user_perms(interaction, "manage_messages")
        if not bot_perms or not user_perms:
            return

        try:
            await message.edit(content=content)
            embed = discord.Embed(
                title="Message Edit Successful",
                description=f"The message has been edited successfully.",
                color=discord.Color.green()
            ).set_footer(
                text=f"Edited by {interaction.user.name}",
                icon_url=interaction.user.avatar
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.Forbidden:
            embed = discord.Embed(
                title="Error",
                description=f"I don't have enough permissions to edit the message.",
                color=discord.Color.red()
            ).set_footer(
                text=f"Requested by {interaction.user.name}",
                icon_url=interaction.user.avatar
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.HTTPException:
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred while editing the message. Please try again later.",
                color=discord.Color.red()
            ).set_footer(
                text=f"Requested by {interaction.user.name}",
                icon_url=interaction.user.avatar
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))