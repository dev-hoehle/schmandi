from datetime import datetime, timedelta
from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands


class moderationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="nickname", description="Changes the bot's or a user's nickname")
    @app_commands.describe(nickname="The nickname you want the bot or user to have")
    @app_commands.describe(member="The member whose nickname you want to change (optional)")
    async def nickname(self, interaction: discord.Interaction, nickname: str = None, member: discord.Member = None):
        if interaction.user.guild_permissions.manage_nicknames:
            if member is None:
                member = interaction.user
            try:
                await member.edit(nick=nickname or member.name)
            except discord.Forbidden:
                await interaction.response.send_message("I don't have the permission to change this member's nickname.")
            else:
                embed = discord.Embed(title="Nickname changed", color=0x00D9FF)
                embed.add_field(name="Changed by ", value=interaction.user.mention)
                embed.add_field(name="Changed to ", value=nickname or member.name)
                await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("You don't have the permission to change nicknames.")


    @app_commands.command(name="clear", description="Deletes a certain number of message")
    @app_commands.describe(amount="The amount of messages to clear")
    async def clear(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
        if interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("Deleted " + str(amount) + " messages", ephemeral=True)
            await interaction.channel.purge(limit=amount)
        else:
            clearembed = discord.Embed(title="Error", color=discord.Color.dark_red(), timestamp=datetime.now())
            clearembed.add_field(name="Something wrent wrong", value=f"<@{interaction.user.id}> you don`t have enough permissions to do that.",)

            await interaction.response.send_message(embed=clearembed, ephemeral=True)


    @app_commands.command(name="poll", description="Creates a simple poll")
    @app_commands.describe(text="Your yes/no question")
    async def poll(self, interaction: discord.Interaction, text: str):
        if interaction.user.guild_permissions.view_audit_log:
            channel = interaction.channel
            channel = discord.utils.get(interaction.guild.channels, name=channel.name)
            embed = discord.Embed(title=text, color=0x00D9FF)
            message = await channel.send(embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            await interaction.response.send_message(f"Ok", ephemeral=True)
        else:
            poolembed = discord.Embed(title="Error", color=discord.Color.dark_red(), timestamp=datetime.now())
            poolembed.add_field(name="Error", value=f"<@{interaction.user.id}> you don't have enough permissions to do that.",)

            await interaction.response.send_message(embed=poolembed, ephemeral=True)


    @app_commands.command(name="say", description="Let the bot say something (Use '\\\\' as linebrake)")
    @app_commands.describe(message="The text you want the bot to say")
    @app_commands.describe(channel="The channel where the message will be sent (optional)")
    async def say(self, interaction: discord.Interaction, message: str, channel: discord.TextChannel = None):
        if "\\" in message:
            message = message.replace("\\", "\n")

        if not interaction.user.guild_permissions.manage_messages:
            embed = discord.Embed(
                title="Error",
                description=f"<@{interaction.user.id}> you don't have enough permissions to do that.",
                color=discord.Color.dark_red(),
                timestamp=datetime.now(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if channel is None:
            channel = interaction.channel

        await channel.send(message)
        await interaction.response.send_message(f"Sent message to {channel.mention}", ephemeral=True)




    @app_commands.command(name="timeout", description="Timeout a Member.")
    @discord.app_commands.describe(member="Who do you want to timeout?")
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, *, time: Literal["15s", "30s", "1min", "5min", "15min", "30min", "1h"], reason: str = None):
        if interaction.user.guild_permissions.manage_members:
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
    await bot.add_cog(moderationCog(bot))
