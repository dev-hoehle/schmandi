from datetime import datetime

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
    @app_commands.describe(amount="The amount of messages to clear (1-100)")
    async def clear(self, interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
        if interaction.user.guild_permissions.manage_messages:
            deleted = await interaction.channel.purge(limit=amount)
            message = f"Deleted {len(deleted)} messages."
            embed = discord.Embed(title="Cleared messages", description=message, color=discord.Color.green())
            embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="Error", color=discord.Color.dark_red(), timestamp=datetime.now())
            embed.add_field(name="Permission Error", value=f"<@{interaction.user.id}> you don't have permission to manage messages.")
            await interaction.response.send_message(embed=embed, ephemeral=True)


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



        

async def setup(bot):
    await bot.add_cog(moderationCog(bot))
