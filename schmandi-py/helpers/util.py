import discord
from discord.ext import commands

def check_member(interaction: discord.Interaction, member: discord.Member = None) -> discord.Member:
    if member == None:
        return interaction.user
    return member