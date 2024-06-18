import discord
from discord.ext import commands

from helpers.config import get_config_value

bot_id = get_config_value("bot_id")

def check_member(interaction: discord.Interaction, member: discord.Member = None) -> discord.Member:
    if member == None:
        return interaction.user
    return member


def check_channel(interaction: discord.Interaction, channel: discord.TextChannel = None) -> discord.TextChannel:
    if channel is None:
        return interaction.channel
    else:
        return channel



async def check_bot_perms(interaction: discord.Interaction, permission_name: str):
    bot_member = interaction.guild.get_member(int(bot_id))


    permissions = bot_member.guild_permissions
    if not getattr(permissions, permission_name):
        embed = discord.Embed(
            title="Permission Denied",
            color=0xff0000
        ).add_field(
            name="Error:",
            value=f"I can`t execute this command. I`m missing permissions: {permission_name}.",
            inline=True
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return False
    else:
        return True

async def check_user_perms(interaction: discord.Interaction, permission_name: str):
    user_member = interaction.guild.get_member(int(interaction.user.id))

    permissions = user_member.guild_permissions
    if not getattr(permissions, permission_name):

        embed = discord.Embed(
            title="Permission Denied",
            color=0xff0000
        ).add_field(
            name="Error:",
            value=f"You can't execute this command. Missing permissions: {permission_name}.",
            inline=True
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return False
    else:
        return True