import discord
from discord.ext import commands
from urllib.parse import urlparse, parse_qs
from helpers.config import get_config_value

bot_id = get_config_value("bot_id")

def check_member(interaction: discord.Interaction, member: discord.User = None) -> discord.User:
    if member == None:
        return interaction.user
    return member


def check_channel(interaction: discord.Interaction, channel: discord.TextChannel = None) -> discord.TextChannel:
    if channel is None:
        return interaction.channel
    else:
        return channel

def isDMChannel(interaction: discord.Interaction) -> bool:
  if isinstance(interaction.channel, discord.DMChannel):
    return True
  return False


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



def get_video_id(url):
    parsed_url = urlparse(url)
    video_id = None

    # Handle standard YouTube URLs
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        if parsed_url.path == "/watch":
            video_id = parse_qs(parsed_url.query).get("v")
            video_id = video_id[0] if video_id else None
        elif parsed_url.path.startswith("/shorts/"):
            video_id = parsed_url.path.split("/")[2] if len(parsed_url.path.split("/")) > 2 else None

    # Handle shared YouTube URLs
    elif parsed_url.hostname in ["youtu.be"]:
        video_id = parsed_url.path[1:]

    if not video_id:
        return None

    return video_id