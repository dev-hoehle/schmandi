from datetime import datetime, timedelta
from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands


class moderationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="nickname", description="Changes the bot's or a user's nickname")
    @app_commands.describe(member="The member whose nickname you want to change (optional)")
    @app_commands.describe(nickname="The nickname you want the bot or user to have")
    async def nickname(self, interaction: discord.Interaction, member: discord.Member = None, nickname: str = None):
        if interaction.user.guild_permissions.manage_nicknames:
            if member is None:
                member = interaction.user

            try:
                await member.edit(nick=nickname or member.name)
            except discord.Forbidden:
                embed = discord.Embed(title="Error", description="I don't have the permission to change this member's nickname.", color=0xFF0000)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            except Exception as e:
                embed = discord.Embed(title="Error", description=f"An error occurred while changing the nickname: {e}", color=0xFF0000)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            embed = discord.Embed(title="Nickname changed", color=0x00D9FF)
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
            embed.add_field(name="Member", value=member.mention, inline=False)
            embed.add_field(name="New Nickname", value=nickname or member.name, inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("You don't have the permission to change nicknames.", ephemeral=True)




    @app_commands.command(name="clear", description="Deletes a certain number of messages")
    @app_commands.describe(amount="The amount of messages to clear")
    async def clear(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
        try:
            # Check if the user has permission to manage channels
            if interaction.user.guild_permissions.manage_channels:
                bot_member = interaction.guild.get_member(self.bot.user.id)
                if bot_member.guild_permissions.manage_messages:
                    await interaction.response.send_message("Messages will be deleted shortly.", ephemeral=True)
                    deleted_messages = await interaction.channel.purge(limit=amount)
                    deleted_messages_count = len(deleted_messages)
                    success_message = f"**__{deleted_messages_count}__** messages have been successfully deleted."
                    failure_message = f"Failed to delete **__{amount - deleted_messages_count}__** messages."

                    embed = discord.Embed(
                        title="Messages Deleted",
                        description=f"{success_message}\n{failure_message}",
                        color=discord.Color.green(),
                        timestamp=datetime.now()
                    )
                    embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar)
                    await interaction.channel.send(embed=embed)
                else:
                    clearembed = discord.Embed(
                        title="Error",
                        color=discord.Color.dark_red(),
                        timestamp=datetime.now()
                    )
                    clearembed.add_field(
                        name="Permission Denied",
                        value=f"I don't have enough permissions to do that.",
                    )
                    await interaction.response.send_message(embed=clearembed, ephemeral=True)
            else:
                clearembed = discord.Embed(
                    title="Error",
                    color=discord.Color.dark_red(),
                    timestamp=datetime.now()
                )
                clearembed.add_field(
                    name="Permission Denied",
                    value=f"<@{interaction.user.id}> you don't have enough permissions to do that.",
                )
                await interaction.response.send_message(embed=clearembed, ephemeral=True)
        except discord.Forbidden:
            error_embed = discord.Embed(
                title="Error",
                description="I do not have permission to perform this action. Please make sure I have the `Manage Messages` permission.",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)
        except discord.HTTPException as e:
            error_embed = discord.Embed(
                title="Error",
                description=f"An error occurred while processing the command. Please try again later. ({e})",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)




    @app_commands.command(name="poll", description="Creates a simple poll")
    @app_commands.describe(text="Your yes/no question")
    async def poll(self, interaction: discord.Interaction, text: str):
        try:
            # Check if the user has permission to manage channels
            if not interaction.user.guild_permissions.manage_channels:
                poolembed = discord.Embed(title="Error", color=discord.Color.dark_red(), timestamp=datetime.now())
                poolembed.add_field(name="Permission Denied", value=f"<@{interaction.user.id}> you don't have enough permissions to do that.")
                await interaction.response.send_message(embed=poolembed, ephemeral=True)
                return

            channel = interaction.channel
            channel = discord.utils.get(interaction.guild.channels, name=channel.name)
            embed = discord.Embed(title=text, color=0x00D9FF)
            message = await channel.send(embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            await interaction.response.send_message("Ok", ephemeral=True)

        except discord.Forbidden:
            error_embed = discord.Embed(title="Error",
                description="I do not have permission to perform this action. Please make sure I have the necessary permissions.",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

        except discord.HTTPException as e:
            error_embed = discord.Embed(title="Error", description=f"An error occurred while processing the command. Please try again later. ({e})",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

        except Exception as e:
            error_embed = discord.Embed(title="Error", description=f"An unexpected error occurred while processing the command. Please try again later. ({e})",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)



    @app_commands.command(name="say", description="Let the bot say something (Use '\\\\' as linebrake)")
    @app_commands.describe(message="The text you want the bot to say")
    @app_commands.describe(channel="The channel where the message will be sent (optional)")
    async def say(self, interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
        if "\\" in message:
            message = message.replace("\\", "\n")

        if not interaction.user.guild_permissions.manage_messages:
            embed = discord.Embed(title="Error", description=f"<@{interaction.user.id}> you don't have enough permissions to do that.", color=discord.Color.dark_red(),
                timestamp=datetime.now(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if channel is None:
            channel = interaction.channel

        try:
            await channel.send(message)
            await interaction.response.send_message(f"Sent message to {channel.mention}", ephemeral=True)
        except discord.Forbidden:
            embed = discord.Embed(title="Error", description="I don't have enough permissions to send messages in that channel.", color=discord.Color.dark_red(),
                timestamp=datetime.now(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except discord.HTTPException:
            embed = discord.Embed(title="Error", description="Failed to send message due to an HTTP error.",
                color=discord.Color.dark_red(),
                timestamp=datetime.now(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)




    @app_commands.command(name="timeout", description="Timeout a Member.")
    @discord.app_commands.describe(member="Who do you want to timeout?")
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, time: Literal["15s", "30s", "1min", "5min", "15min", "30min", "1h"], *, reason: str = None):

        # Check if the user has the manage_roles permission to execute the command
        if not interaction.user.guild_permissions.manage_roles:
            embed = discord.Embed(title="Timeout failed", color=0xff0000)
            embed.add_field(name="Error", value="You do not have permission to use this command.", inline=True,)
            return await interaction.response.send_message( embed=embed, ephemeral=True)

        # Map the timeout durations to seconds
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
            # Save the original timeout duration before converting it to seconds
            oldtime = time
            time = timemap[time]
        except KeyError:
            embed = discord.Embed(title="Timeout failed", color=0xff0000)
            embed.add_field(name="Error", value="Invalid timeout duration specified.", inline=True,
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        # Convert the timeout duration to a timedelta object
        timeout_duration = timedelta(seconds=int(time))

        try:
            timeout_result = await member.timeout(timeout_duration)
        except discord.errors.Forbidden:
            embed = discord.Embed(title="Timeout failed", color=0xff0000)
            embed.add_field(name="Error", value="You do not have permission to use this command.", inline=True,)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(title="Timeout failed", color=0xff0000)
            embed.add_field(name="Error", value=f"{e}", inline=True)
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        embed = discord.Embed(title="Timeout Successful", color=0x00D9FF)
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="Duration", value=f"{oldtime}", inline=True)
        embed.add_field(name="Reason", value=f"{reason}", inline=True)
        await interaction.response.send_message(embed=embed)

        # Send a DM to the timed-out user
        embed = discord.Embed(title=f"You have been timed out in **{interaction.guild.name}**!", color=0x00D9FF,)
        embed.add_field(name="Timed out by", value=interaction.user.mention)
        embed.add_field(name="Duration", value=f"{oldtime}")
        embed.add_field(name="Reason", value=f"{reason}")
        try:
            await member.send(embed=embed)
        except discord.errors.Forbidden:
            pass


async def setup(bot):
    await bot.add_cog(moderationCog(bot))
